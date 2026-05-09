## MODIFIED Requirements

### Requirement: RAG Agent REST API
The system SHALL expose the RAG agent's chat capabilities via a FastAPI REST endpoint, with configuration that defaults to a neutral stewardship guide persona.

#### Scenario: Streaming Chat Response with History
- **WHEN** an authenticated client sends a POST request to `/chat` with a query prompt and a list of previous messages (history)
- **THEN** the API SHALL stream the response back from the RAG agent using Server-Sent Events (SSE), ensuring the agent considers the provided history for context.
- **AND** the API SHALL process this request asynchronously, allowing the server to handle concurrent requests (e.g., health checks) while the stream is active.
- **AND** the system instruction SHALL use a generic "Stewardship Guide" identity if no specific organization name is provided in the configuration.
