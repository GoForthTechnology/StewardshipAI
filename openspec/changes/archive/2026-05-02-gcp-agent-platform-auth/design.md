## Context

The current `GCPRagAgent` implementation is brittle due to hardcoded project IDs and a manual try-except block for authentication. When deploying to GCP's agent platform, the environment provides the necessary identity and configuration. We need to align the agent's initialization with these platform-native patterns.

## Goals / Non-Goals

**Goals:**
- **Externalize Configuration**: All environment-specific details (project, location, corpus ID) must be configurable via environment variables.
- **Unified Authentication**: Use a consistent strategy for obtaining credentials that works seamlessly in local development and production.
- **Type Safety**: Use `pydantic` for validating configuration at startup.

**Non-Goals:**
- Changing the core RAG logic or prompt instructions.
- Supporting non-GCP RAG providers.

## Decisions

- **Configuration Management**: Use a `GCPConfig` class inheriting from `pydantic_settings.BaseSettings` (or a standard `BaseModel` if `pydantic-settings` is not available) to manage environment variables.
- **Environment Variables**:
    - `GCP_PROJECT_ID`: The GCP project ID or number.
    - `GCP_LOCATION`: The Vertex AI location (e.g., `us-south1`).
    - `GCP_RAG_CORPUS_ID`: The full resource name or ID of the RAG corpus.
- **Authentication Strategy**:
    - If `GOOGLE_CLOUD_API_KEY` is set, use it.
    - Otherwise, default to ADC (which handles `GOOGLE_APPLICATION_CREDENTIALS` or metadata server identities).
    - Simplify `GCPRagAgent.__init__` by removing the manual `subprocess` call for `gcloud` tokens, as the SDK and standard ADC libraries handle this more reliably when configured correctly.

## Risks / Trade-offs

- **[Risk]** Missing Env Vars → **[Mitigation]** `pydantic` will raise a clear validation error on initialization if required fields are missing.
- **[Risk]** Local Auth Confusion → **[Mitigation]** Provide clear documentation on which variables to set for different auth modes.
