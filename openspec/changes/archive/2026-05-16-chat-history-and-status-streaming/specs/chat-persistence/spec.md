## ADDED Requirements

### Requirement: Local-First Chat Persistence
The system SHALL provide a mechanism to persist chat sessions locally on the user's device, enabling users to view and resume past conversations across page reloads without requiring a backend database.

#### Scenario: Saving a Chat Session
- **WHEN** a new message is added to a chat
- **THEN** the system SHALL update the corresponding session in `localStorage` with the full message history and metadata.

#### Scenario: Loading Recent Chats
- **WHEN** the portal loads
- **THEN** the system SHALL retrieve the list of recent chat sessions from `localStorage` and display them in the sidebar.

#### Scenario: Resuming a Previous Chat
- **WHEN** a user selects a chat session from the history sidebar
- **THEN** the system SHALL clear the current chat view and load the messages and persona state from the selected session.

### Requirement: Chat Session Titling
The system SHALL support assigning descriptive titles to chat sessions based on the content of the initial exchange.

#### Scenario: Initializing a Chat Title
- **WHEN** a new chat session is created
- **THEN** the system SHALL initially set the title to a placeholder (e.g., "New Chat").
- **AND** after the first turn completes, the system SHALL trigger an asynchronous request to generate a concise, relevant title.
