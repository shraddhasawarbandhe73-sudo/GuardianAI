# GuardianAI Demo Video Plan (under 3 minutes)

IMPORTANT: Record only after the Ring Developer Playground integration is actually working. The final video must show a real Ring simulator/API interaction. Demo-mode-only footage is not enough for the Ring track. Never show the Ring access token, `.env`, AWS credentials, or private personal data.

## 0:00–0:20 — Intro
"Hello, this is GuardianAI, a caregiver-focused event triage dashboard for the Ring ecosystem. It helps turn household event metadata into clearer alerts for human review."

## 0:20–0:45 — Problem
"Raw motion alerts can lack context. GuardianAI presents event information with a concise summary and a priority level, while keeping the caregiver responsible for verifying what happened."

## 0:45–1:15 — Ring integration
Show the Ring Developer Playground/device source and then switch to GuardianAI. Click Load Ring Devices, select a device, and load event history. Make it clear this is live Ring API data from the simulator/device.

## 1:15–1:55 — Dashboard
Show event history, priority badges, summaries, and the analysis method. Explain whether the result used Bedrock or the rule-based fallback.

## 1:55–2:25 — Test
Use the test-event form to demonstrate one example. Clearly label this as a test event rather than real household data.

## 2:25–2:45 — Technical detail
Briefly show the source repository and explain the backend, Ring event-history call, and optional Bedrock path if it was actually configured and tested.

## 2:45–2:58 — Close
"GuardianAI aims to make household event notifications easier to understand while keeping people in control. Thank you."

## Recording
Use Windows + Alt + R if Xbox Game Bar supports the browser window, or use another screen recorder. Upload the final video publicly to YouTube or Vimeo, in English, under three minutes.
