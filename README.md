# GuardianAI — Ring Care & Safety Intelligence

GuardianAI is a prototype that turns Ring event metadata into a concise, human-reviewed activity triage dashboard. It supports:
- Demo mode with explicitly simulated events.
- Ring API device discovery and event history when a valid Ring Developer Playground access token is configured.
- Optional Amazon Bedrock event summaries when AWS credentials and a model ID are configured.
- A transparent rule-based fallback so the app still runs without cloud credentials.

## Important honesty and safety notes
- Demo mode data is simulated, not live Ring data.
- The fallback classifier is rule-based, not a trained AI model.
- Amazon Bedrock is only used if `BEDROCK_MODEL_ID` and valid AWS credentials are configured.
- The app does not detect or confirm falls, diagnose medical conditions, or replace emergency services.
- Do not commit `.env`, access tokens, credentials, private footage, or personal information.
- Do not claim a live Ring integration in the final video unless you actually configure a token and show Ring events being retrieved.

## Run on Windows
1. Install Python 3.10 or later.
2. Extract this folder.
3. Double-click `RUN_GUARDIANAI.bat`.
4. The browser opens at `http://127.0.0.1:5000`.
5. Click **Use Demo Events** to test the interface.

## Configure Ring Developer Playground
1. Open the official Ring Developer Playground from the Ring Developer portal/resources.
2. Generate a temporary access token.
3. Stop the app.
4. Open `.env` in Notepad and set `RING_ACCESS_TOKEN=PASTE_TOKEN_HERE`.
5. Restart `RUN_GUARDIANAI.bat`.
6. Click **Load Ring Devices**, choose a device, then **Load Device Event History**.
7. Tokens expire; generate a new one when needed. Never show the token in a screen recording.

The backend uses the Ring API endpoints documented by Amazon's `AmazonAppDev/ring-api-helloworld` starter:
- `GET /v1/devices`
- `GET /v1/history/devices/{device_id}/events`

## Optional Amazon Bedrock
1. Configure AWS credentials on your machine using the official AWS CLI setup, or the environment variables supported by boto3.
2. Ensure your AWS account has access to a Bedrock model in your chosen region.
3. Set `AWS_REGION` and `BEDROCK_MODEL_ID` in `.env`.
4. Restart the app and verify the status message says Bedrock is configured.
5. Test and record only after checking actual outputs. AWS usage may incur charges depending on account and model.

If Bedrock is not configured, the app uses a transparent rule-based fallback. Do not select the AWS Builder mini-challenge until you have actually integrated and tested an AWS service and documented it.

## API routes
- `GET /api/status`
- `GET /api/devices`
- `GET /api/events?device_id=...`
- `GET /api/demo-events`
- `POST /api/analyze`

## Devpost preparation
- Project track: Ring.
- Submit a public GitHub repository with an open-source license or make the repo private and invite the required reviewers.
- Include a public English demo video under 3 minutes.
- The demo video must show the app working through the Ring Developer Playground simulator or an actual Ring device.
- Complete honest product feedback for every tool/API/SDK actually used.
- Replace all placeholders and claims with what you actually tested.
