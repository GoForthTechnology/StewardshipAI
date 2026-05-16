## MODIFIED Requirements

### Requirement: Branded Portal Layout
The web interface SHALL use a modern component-based layout (Angular) to implement a high-fidelity, responsive design that is clean, professional, and organizationally neutral, adapting its structure based on the user's device.

#### Scenario: Displaying Generic Branding
- **WHEN** the application loads
- **THEN** it SHALL show the "Stewardship Portal" title and generic branding elements, with NO mention of any specific diocese.

#### Scenario: Header Title Display
- **WHEN** the application loads
- **THEN** the header SHALL show "Stewardship Portal" with the Dove icon.

#### Scenario: Displaying Responsive Layout
- **WHEN** the application loads
- **THEN** it SHALL detect the screen size and display either a permanent sidebar (desktop) or a collapsible drawer with a top header (mobile).
- **AND** the sidebar SHALL include a dedicated section for "Recent Chats".

### Requirement: Animated Request Pending State
The web interface SHALL display dynamic status updates and animated visual feedback when a message has been sent and is awaiting a response from the agent.

#### Scenario: Visual Feedback for Pending Message
- **WHEN** a user submits a query
- **THEN** the system SHALL display a chat bubble containing three animated dots.
- **AND** if the backend sends a status update, the system SHALL display that status text (e.g., "Searching...") alongside or within the animated bubble.
- **AND** the status UI SHALL disappear once the first text chunk of the agent response is received.

## ADDED Requirements

### Requirement: Chat History Navigation
The web interface SHALL allow users to browse and select from their list of local chat sessions in the sidebar.

#### Scenario: Selecting a Recent Chat
- **WHEN** a user clicks a chat title in the "Recent Chats" sidebar
- **THEN** the interface SHALL load that specific session's history and set the current persona context accordingly.
