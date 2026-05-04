## ADDED Requirements

### Requirement: RAG Agent REST API
The system SHALL expose the RAG agent's chat capabilities via a FastAPI REST endpoint.

#### Scenario: Streaming Chat Response
- **WHEN** an authenticated client sends a POST request to `/chat` with a query prompt
- **THEN** the API SHALL stream the response back from the RAG agent using Server-Sent Events (SSE) or a streaming JSON response.

### Requirement: API Authentication Middleware
The API SHALL require a valid Firebase ID token in the `Authorization` header for all requests to protected endpoints.

#### Scenario: Rejecting Unauthenticated Requests
- **WHEN** a client sends a request without a valid Bearer token
- **THEN** the API SHALL return a 401 Unauthorized status.
