# GuardianAI — AI-Assisted Care & Safety Intelligence for Ring

## Tagline
Turning Ring events into context-aware alerts for the people who care.

## What it does
GuardianAI is a caregiver-focused dashboard for interpreting household activity events. It aims to reduce notification noise by grouping event metadata into Normal, Attention, or Urgent triage levels and showing a short explanation for a human to review.

## The problem
Security systems can notify users that motion or another event occurred, but a raw notification may not explain whether the activity was expected or needs attention. Caregivers need clear, cautious context rather than a stream of unexplained alerts.

## How it works
GuardianAI can load event history from Ring's developer API when configured with a valid Ring Developer Playground access token. The backend analyzes event metadata and displays the result in a browser dashboard. It includes a demo mode for interface testing. If configured with AWS credentials and an accessible Amazon Bedrock model, the backend can use Bedrock to summarize event metadata; otherwise it uses a transparent rule-based fallback.

## What makes it different
The focus is on caregiver-friendly context and triage, not simply displaying a motion alert. It explicitly shows whether the result came from Amazon Bedrock or the rule-based fallback so the demo can be transparent about what was actually used.

## Safety
GuardianAI is an experimental awareness tool, not a medical device or emergency service. It does not confirm falls or diagnose a person's condition. A human must verify events and decide what action to take.

## Track
Ring.

## AWS Builder mini-challenge
Select only if Amazon Bedrock or another qualifying AWS service is actually configured, integrated, tested, and described in the submitted code. Otherwise do not select AWS Builder.

## Important before submitting
The final submission must be consistent with the tested version. Include the actual public GitHub URL, the public English demo video under three minutes, and honest product feedback. The demo must show real operation through the Ring Developer Playground simulator or a Ring device; simulated GuardianAI demo events alone do not satisfy the Ring integration requirement.
