## ADDED Requirements

### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API.

#### Scenario: Submitting a Query
- **WHEN** an authenticated user enters a question into the chat input and presses send
- **THEN** the system SHALL display the user's message and initiate a streaming response from the backend API that focuses exclusively on text content.

### Requirement: Branded Portal Layout
The web interface SHALL use a modern component-based layout (Angular) to implement a high-fidelity, responsive design matching the "Catholic Diocese of Wichita" branding and ecclesiastical stewardship theme.

#### Scenario: Displaying Diocesan Branding
- **WHEN** the application loads
- **THEN** it SHALL show the "Catholic Diocese of Wichita Stewardship Portal" title and branding elements.

#### Scenario: Responsive Display
- **WHEN** viewed on mobile or desktop devices
- **THEN** the layout SHALL adapt fluidly while maintaining brand contrast and readability.

### Requirement: Persona Selection
The web interface SHALL provide a clear mechanism for users to select whether they are interacting as a "Parishioner" or a "Priest/Leader".

#### Scenario: Selecting a Persona
- **WHEN** a user selects a persona from the toggle or radio buttons
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
