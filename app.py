import os
import re
from datetime import datetime, timezone
from flask import Flask, jsonify, request, send_from_directory
import requests

try:
    import boto3
except Exception:
    boto3 = None

APP_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder="static")
RING_BASE_URL = os.getenv("RING_API_BASE_URL", "https://api.amazonvision.com").rstrip("/")
RING_ACCESS_TOKEN = os.getenv("RING_ACCESS_TOKEN", "").strip()
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "").strip()
REQUEST_TIMEOUT = 20

def classify_event(event):
    """Safe, transparent fallback classifier; not a medical detector."""
    raw = " ".join(str(event.get(k, "")) for k in (
        "event_type", "type", "kind", "description", "name", "source",
        "classification", "object_type", "label"
    )).lower()
    ts = event.get("timestamp") or event.get("created_at") or event.get("time") or ""
    score = 15
    reasons = []
    urgent_words = ("fall", "person_down", "distress", "forced_entry", "break_in")
    attention_words = ("motion", "vehicle", "package", "doorbell", "person", "human", "animal", "unknown")
    if any(w in raw for w in urgent_words):
        score = 85
        reasons.append("Event text contains a potentially high-priority indicator.")
    elif any(w in raw for w in attention_words):
        score = 48
        reasons.append("Motion or activity event may need a quick human review.")
    else:
        reasons.append("No high-priority indicator was found in the available event metadata.")
    if "doorbell" in raw or "package" in raw or "vehicle" in raw:
        score = max(score, 45)
    level = "URGENT" if score >= 75 else ("ATTENTION" if score >= 35 else "NORMAL")
    summary = {
        "level": level,
        "score": score,
        "summary": {
            "URGENT": "Potentially important event. Check the live context promptly.",
            "ATTENTION": "Activity detected. Check whether it was expected.",
            "NORMAL": "No obvious high-priority indicator in the available metadata."
        }[level],
        "reason": " ".join(reasons),
        "method": "transparent rule-based fallback"
    }
    return summary

def bedrock_summary(event, fallback):
    """Optional real LLM path when AWS credentials and model ID are configured."""
    if not BEDROCK_MODEL_ID or boto3 is None:
        return fallback
    try:
        client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
        prompt = (
            "You are a cautious home-event triage assistant. You are NOT a medical or emergency diagnosis system. "
            "Do not infer a fall or medical state unless explicit metadata says so. Use only the event metadata provided. "
            "Return JSON with keys level (NORMAL, ATTENTION, URGENT), summary (one sentence), reason (one sentence). "
            "Use URGENT only for explicit strong danger indicators; otherwise prefer ATTENTION or NORMAL. "
            "Event metadata: " + json.dumps(event, ensure_ascii=False)[:4000]
        )
        response = client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 250, "temperature": 0.1}
        )
        text = response["output"]["message"]["content"][0]["text"]
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            return fallback
        data = json.loads(match.group(0))
        level = str(data.get("level", "ATTENTION")).upper()
        if level not in ("NORMAL", "ATTENTION", "URGENT"):
            level = "ATTENTION"
        return {
            "level": level,
            "score": {"NORMAL": 15, "ATTENTION": 48, "URGENT": 80}[level],
            "summary": str(data.get("summary", fallback["summary"]))[:300],
            "reason": str(data.get("reason", fallback["reason"]))[:300],
            "method": "Amazon Bedrock"
        }
    except Exception as exc:
        # Keep the app usable and never leak credentials.
        fallback["ai_note"] = "Bedrock unavailable; using the transparent fallback classifier."
        return fallback

def analyze_event(event):
    return bedrock_summary(event, classify_event(event))

def ring_request(path):
    if not RING_ACCESS_TOKEN:
        raise RuntimeError("Ring token not configured. Add RING_ACCESS_TOKEN to .env, or use Demo Mode.")
    response = requests.get(
        f"{RING_BASE_URL}{path}",
        headers={"Authorization": f"Bearer {RING_ACCESS_TOKEN}", "Accept": "application/json"},
        timeout=REQUEST_TIMEOUT
    )
    if response.status_code == 401:
        raise RuntimeError("Ring token is invalid or expired. Generate a fresh token in Ring Developer Playground.")
    response.raise_for_status()
    return response.json()

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/api/status")
def status():
    return jsonify({
        "ring_configured": bool(RING_ACCESS_TOKEN),
        "bedrock_configured": bool(BEDROCK_MODEL_ID and boto3 is not None),
        "mode": "Ring API + optional Bedrock" if RING_ACCESS_TOKEN else "Demo Mode"
    })

@app.get("/api/devices")
def devices():
    try:
        data = ring_request("/v1/devices")
        return jsonify({"ok": True, "data": data})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.get("/api/events")
def events():
    device_id = request.args.get("device_id", "").strip()
    if not device_id:
        return jsonify({"ok": False, "error": "Choose a Ring device first."}), 400
    # Endpoint path is from AmazonAppDev's official Ring API hello-world sample.
    safe_id = requests.utils.quote(device_id, safe=".")
    try:
        data = ring_request(f"/v1/history/devices/{safe_id}/events")
        raw_events = data if isinstance(data, list) else data.get("events", data.get("data", []))
        enriched = []
        for event in raw_events[:100]:
            item = dict(event) if isinstance(event, dict) else {"event": str(event)}
            item["guardian_analysis"] = analyze_event(item)
            enriched.append(item)
        return jsonify({"ok": True, "events": enriched, "count": len(enriched)})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

@app.post("/api/analyze")
def analyze():
    event = request.get_json(silent=True) or {}
    if not isinstance(event, dict):
        return jsonify({"ok": False, "error": "Send a JSON object."}), 400
    result = analyze_event(event)
    return jsonify({"ok": True, "analysis": result})

@app.get("/api/demo-events")
def demo_events():
    now = datetime.now(timezone.utc).isoformat()
    demo = [
        {"event_type": "motion_detected", "device_name": "Front Door", "timestamp": now, "description": "Motion detected near the entrance"},
        {"event_type": "package_delivery", "device_name": "Front Door", "timestamp": now, "description": "Package delivery activity"},
        {"event_type": "device_status", "device_name": "Living Room", "timestamp": now, "description": "Routine device status update"}
    ]
    return jsonify({"ok": True, "events": [
        {**e, "guardian_analysis": analyze_event(e), "demo": True} for e in demo
    ]})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
