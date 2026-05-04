## MODIFIED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API.

#### Scenario: Submitting a Query
- **WHEN** an authenticated user enters a question into the chat input and presses send
- **THEN** the system SHALL display the user's message and initiate a streaming response from the backend API that focuses exclusively on text content.

## REMOVED Requirements

### Requirement: Citation Visibility
**Reason**: Replaced by a more conversational, direct response model without external source links or footnotes.
**Migration**: Remove citation rendering components and the `citations` field from the chat message model.
