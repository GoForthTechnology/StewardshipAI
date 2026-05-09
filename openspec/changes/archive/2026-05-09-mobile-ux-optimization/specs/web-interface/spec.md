## MODIFIED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API, optimized for both desktop and mobile devices.

#### Scenario: Submitting a Query on Mobile
- **WHEN** an authenticated user on a mobile device enters a question into the chat input
- **THEN** the system SHALL display the user's message and ensure the input area remains accessible and visible even when the mobile keyboard is active.

### Requirement: Branded Portal Layout
The web interface SHALL use a modern component-based layout (Angular) to implement a high-fidelity, responsive design that is clean, professional, and organizationally neutral, adapting its structure based on the user's device.

#### Scenario: Displaying Responsive Layout
- **WHEN** the application loads
- **THEN** it SHALL detect the screen size and display either a permanent sidebar (desktop) or a collapsible drawer with a top header (mobile).
