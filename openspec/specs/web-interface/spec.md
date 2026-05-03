## ADDED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface that allowing users to send text queries and receive grounded responses from the RAG agent.

#### Scenario: Submitting a Query
- **WHEN** an authenticated user enters a question into the chat input and presses send
- **THEN** the system SHALL display the user's message and initiate a streaming response from the agent.

### Requirement: Citation Visibility
The web interface SHALL display citations for every claim made by the agent, linking to the source metadata.

#### Scenario: Viewing Citations
- **WHEN** the agent provides a response containing citations
- **THEN** the system SHALL render these citations in a readable format (e.g., footnotes or sidebar references).
