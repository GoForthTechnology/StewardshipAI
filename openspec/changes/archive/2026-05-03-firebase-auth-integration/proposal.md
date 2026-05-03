## Why

The current authentication in StewardshipAI is a simulation that relies on simple text input and manual trust. To ensure the security and integrity of the research agent for internal development, we need to implement a production-ready, zero-cost authentication layer using Firebase (Google Identity Platform). This will enforce real identity verification before any interaction with the RAG agent occurs.

## What Changes

- **Firebase Integration**: Replace the simulated text-input login with a real Google SSO flow powered by the Firebase JavaScript SDK.
- **Backend Verification**: Implement server-side JWT token verification using `firebase-admin` to ensure user identities are valid.
- **Infrastructure as Code**: Update Terraform to enable Identity Platform and configure Google as a sign-in provider.
- **User Identification**: Modify the RAG agent to identify the user in each interaction for auditing purposes.

## Capabilities

### New Capabilities
- `user-audit-logging`: Tracking user interactions with the agent for stewardship oversight.

### Modified Capabilities
- `user-authentication`: Transitioning from simulated to real Firebase-backed authentication and allow-list enforcement.
- `iac-provisioning`: Adding Identity Platform and OAuth configuration to the infrastructure setup.

## Impact

- **app.py**: Major refactor of the authentication UI and session management.
- **config.py**: New environment variables for Firebase API keys and Project IDs.
- **rag_agent.py**: Addition of user identity context in generation requests.
- **terraform/**: New resources for Identity Platform and Google Provider configuration.
- **dependencies**: Full utilization of `firebase-admin` (already in requirements.txt).
