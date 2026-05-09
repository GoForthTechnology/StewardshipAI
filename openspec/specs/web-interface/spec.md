## ADDED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API.

#### Scenario: Submitting a Query
- **WHEN** an authenticated user enters a question into the chat input and presses send
- **THEN** the system SHALL display the user's message and initiate a streaming response from the backend API that focuses exclusively on text content.

#### Scenario: Submitting a Follow-up Query
- **WHEN** an authenticated user enters a question into the chat input
- **THEN** the system SHALL send the new question along with the current session's message history to the backend.
- **AND** the system SHALL update the chat display to include the full conversational history.

### Requirement: Branded Portal Layout
The web interface SHALL use a modern component-based layout (Angular) to implement a high-fidelity, responsive design matching the "Catholic Diocese of Wichita" branding and ecclesiastical stewardship theme.

#### Scenario: Displaying Diocesan Branding
- **WHEN** the application loads
- **THEN** it SHALL show the "Catholic Diocese of Wichita Stewardship Portal" title and branding elements.

#### Scenario: Responsive Display
- **WHEN** viewed on mobile or desktop devices
- **THEN** the layout SHALL adapt fluidly while maintaining brand contrast and readability.

### Requirement: Persona Selection
The web interface SHALL provide a clear mechanism for users to select whether they are interacting as a "Parishioner", a "Priest/Leader", or an "Academic / Researcher".

#### Scenario: Selecting a Persona
- **WHEN** a user selects a persona from the toggle, sidebar buttons, or other selection mechanism
- **THEN** the system SHALL update the session state and pass this context to the RAG agent for subsequent queries.

### Requirement: Quick-Start Discovery Actions
The web interface SHALL present "Quick-Start" buttons or cards for common stewardship categories to help users discover content.

#### Scenario: Triggering a Quick-Start Query
- **WHEN** a user clicks a discovery button (e.g., "Explain Tithing")
- **THEN** the system SHALL automatically submit that query to the agent on behalf of the user.

### Requirement: Enhanced Markdown Rendering
The web interface SHALL render markdown content with consistent spacing and indentation for structural elements.

#### Scenario: Displaying Lists
- **WHEN** a chat message containing a list is rendered
- **THEN** the system SHALL apply appropriate margins and padding to the list items to ensure they are distinct and easy to read.

### Requirement: Animated Request Pending State
The web interface SHALL display an animated ellipsis ("...") visual feedback when a message has been sent and is awaiting a response from the agent.

#### Scenario: Visual Feedback for Pending Message
- **WHEN** a user submits a query
- **THEN** the system SHALL display a chat bubble containing three animated dots that bounce or pulse to indicate the request is being processed.
- **AND** the animated bubble SHALL disappear once the first chunk of the agent response is received.

### Requirement: Frontend Request Timeout
The web interface SHALL implement a client-side timeout for chat generation requests to prevent the UI from appearing hung.

#### Scenario: Frontend Request Timeout
- **WHEN** a chat generation request does not receive a response within 15 seconds
- **THEN** the interface SHALL abort the request and display a specific timeout error message to the user.

### Requirement: Differentiated Error Feedback
The web interface SHALL provide specific visual feedback for different types of request failures.

#### Scenario: Displaying Timeout Error
- **WHEN** a request is aborted due to a timeout
- **THEN** the system SHALL display a message like "The request took too long. Please try again."

#### Scenario: Displaying Generic Error
- **WHEN** a request fails due to any other network or server error
- **THEN** the system SHALL display a message like "I encountered an error connecting to our resources. Please try again later."
