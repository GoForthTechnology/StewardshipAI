## Why

To allow external testers to engage with the StewardshipAI agent safely and easily, we need a web-based user interface protected by a robust authentication layer. This ensures only authorized individuals can access the prototype, preventing unauthorized usage and managing infrastructure costs.

## What Changes

- Implementation of a Streamlit-based web UI for the research agent.
- Integration of Firebase Authentication (Google SSO) to restrict access.
- Implementation of a server-side "Allow-List" to authorize specific Gmail accounts.
- Transition of the agent from a local CLI tool to a containerized service deployed on Google Cloud Run.

## Capabilities

### New Capabilities
- `web-interface`: A conversational web UI built with Streamlit for interacting with the RAG agent.
- `user-authentication`: Identity verification using Firebase Auth and an email allow-list to control access.

### Modified Capabilities
- `gcp-rag-agent`: Modification to support session-based interactions and audit logging via user identity.

## Impact

- New dependencies: `streamlit`, `firebase-admin`, `google-auth`.
- New infrastructure: Google Cloud Run service, Firebase Project (Identity Platform), and IAM policy updates.
- Migration from `agent.py` (CLI) as the primary interface to `app.py` (Web).
