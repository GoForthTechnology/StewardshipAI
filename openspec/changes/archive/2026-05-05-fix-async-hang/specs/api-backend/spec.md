## MODIFIED Requirements

### Requirement: RAG Agent REST API
The system SHALL expose the RAG agent's chat capabilities via a FastAPI REST endpoint.

#### Scenario: Streaming Chat Response with History
- **WHEN** an authenticated client sends a POST request to `/chat` with a query prompt and a list of previous messages (history)
- **THEN** the API SHALL stream the response back from the RAG agent using Server-Sent Events (SSE), ensuring the agent considers the provided history for context.
- **AND** the API SHALL process this request asynchronously, allowing the server to handle concurrent requests (e.g., health checks) while the stream is active.

## ADDED Requirements

### Requirement: Backend Request Timeout
The API SHALL enforce a maximum time limit on the total duration of a chat generation request.

#### Scenario: Generation Request Timeout
- **WHEN** a chat generation request takes longer than 60 seconds
- **THEN** the API SHALL terminate the request and yield an error message to the client indicating a timeout.
