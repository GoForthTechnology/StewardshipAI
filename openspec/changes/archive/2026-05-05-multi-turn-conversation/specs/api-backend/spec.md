## MODIFIED Requirements

### Requirement: RAG Agent REST API
The system SHALL expose the RAG agent's chat capabilities via a FastAPI REST endpoint.

#### Scenario: Streaming Chat Response with History
- **WHEN** an authenticated client sends a POST request to `/chat` with a query prompt and a list of previous messages (history)
- **THEN** the API SHALL stream the response back from the RAG agent using Server-Sent Events (SSE), ensuring the agent considers the provided history for context.
