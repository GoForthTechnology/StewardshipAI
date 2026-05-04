## MODIFIED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API.

#### Scenario: Submitting a Query
- **WHEN** an authenticated user enters a question into the chat input and presses send
- **THEN** the system SHALL display the user's message and initiate a streaming response from the backend API.

### Requirement: Citation Visibility
The Angular web interface SHALL display citations for every claim made by the agent, linking to the source metadata.

#### Scenario: Viewing Citations
- **WHEN** the API provides a response containing citations
- **THEN** the system SHALL render these citations in a readable format (e.g., footnotes or sidebar references) within the Angular UI.

## ADDED Requirements

### Requirement: Modern Branded Layout
The web interface SHALL use a modern component-based layout (Angular) to implement a high-fidelity, responsive design matching the Diocese of Wichita's branding.

#### Scenario: Responsive Display
- **WHEN** viewed on mobile or desktop devices
- **THEN** the layout SHALL adapt fluidly while maintaining brand contrast and readability.
