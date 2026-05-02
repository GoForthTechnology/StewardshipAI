## Why

The current implementation of the `GCPRagAgent` relies on a hardcoded project ID and location, and uses a fragile try-except pattern for authentication fallback. This approach is difficult to manage when deploying to GCP's agent platform (such as Vertex AI Agent Builder or Cloud Run), where identity and configuration should be environment-driven and platform-native.

## What Changes

- **Externalize Configuration**: Move project ID, location, and RAG corpus ID to environment variables or a configuration object.
- **Robust Authentication**: Implement a cleaner credential provider that prioritizes platform-native identity (ADC) in production while allowing Service Account keys or API keys for local development.
- **Support Service Account Keys**: Add explicit support for `GOOGLE_APPLICATION_CREDENTIALS` to allow local testing without requiring `gcloud auth login`.
- **Remove Hardcoding**: Eliminate hardcoded strings for project `YOUR_PROJECT_ID` and location `us-south1`.

## Capabilities

### New Capabilities
- `gcp-agent-auth`: A standardized authentication and configuration module for GCP-deployed agents.

### Modified Capabilities
- `gcp-rag-agent`: Refactor to use the new `gcp-agent-auth` capability instead of internal fallback logic.

## Impact

- `rag_agent.py`: Significant refactoring of the `__init__` method and configuration handling.
- Environment: Requires setting `GCP_PROJECT`, `GCP_LOCATION`, and `GCP_RAG_CORPUS` (or similar) for the agent to function correctly without manual overrides.
