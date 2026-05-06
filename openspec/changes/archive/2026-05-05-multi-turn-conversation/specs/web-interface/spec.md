## MODIFIED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API.

#### Scenario: Submitting a Follow-up Query
- **WHEN** an authenticated user enters a question into the chat input
- **THEN** the system SHALL send the new question along with the current session's message history to the backend.
- **AND** the system SHALL update the chat display to include the full conversational history.
