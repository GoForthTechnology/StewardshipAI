## ADDED Requirements

### Requirement: Granular Status Yielding
The RAG agent SHALL yield discrete status updates during its internal processing lifecycle, particularly during long-running tasks like RAG retrieval and document analysis.

#### Scenario: Yielding RAG Retrieval Status
- **WHEN** the agent starts the retrieval phase
- **THEN** it SHALL yield a status message such as "🔍 Searching official resources...".

#### Scenario: Yielding Persona-Aware Source Feedback
- **WHEN** the agent is in the "Researcher" persona and identifies relevant documents
- **THEN** it SHALL yield a status message identifying the specific document names (e.g., "📖 Analyzing: Volunteer Handbook 2026.pdf").

### Requirement: Multiplexed SSE Stream
The backend API SHALL use a single Server-Sent Events (SSE) stream to deliver both internal status updates and the final generative text chunks as distinct JSON objects.

#### Scenario: Streaming Mixed Content
- **WHEN** the agent processes a request
- **THEN** the API SHALL emit one or more JSON objects with a `status` key.
- **AND** follow them with multiple JSON objects with a `text` key as the generation proceeds.
