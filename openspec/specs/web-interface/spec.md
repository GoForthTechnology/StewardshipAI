# Web Interface Specification

## Purpose
Define the requirements for the user-facing web portal and its interactive elements.
## Requirements
### Requirement: Conversational Web Interface
The system SHALL provide a web-based chat interface (built in Angular) allowing users to send text queries and receive grounded responses from the RAG API, optimized for both desktop and mobile devices.

#### Scenario: Submitting a Query
- **WHEN** an authenticated user enters a question into the chat input and presses send
- **THEN** the system SHALL display the user's message and initiate a streaming response from the backend API that focuses exclusively on text content.

#### Scenario: Submitting a Follow-up Query
- **WHEN** an authenticated user enters a question into the chat input
- **THEN** the system SHALL send the new question along with the current session's message history to the backend.
- **AND** the system SHALL update the chat display to include the full conversational history.

#### Scenario: Submitting a Query on Mobile
- **WHEN** an authenticated user on a mobile device enters a question into the chat input
- **THEN** the system SHALL display the user's message and ensure the input area remains accessible and visible even when the mobile keyboard is active.

### Requirement: Persona Selection and Display
The web interface SHALL provide a clear mechanism for users to select whether they are interacting as a "Parishioner", a "Priest/Leader", or an "Academic / Researcher" located in the chat header.

#### Scenario: Selecting a Persona
- **WHEN** a user selects a persona from the header switcher
- **THEN** the system SHALL update the session state and pass this context to the RAG agent for subsequent queries.

#### Scenario: Switching Personas
- **WHEN** user selects a new persona from the header navigation
- **THEN** the interface SHALL update the active persona indicator and adjust the suggested prompts in the Discovery Grid.

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
The web interface SHALL display dynamic status updates and animated visual feedback when a message has been sent and is awaiting a response from the agent.

#### Scenario: Visual Feedback for Pending Message
- **WHEN** a user submits a query
- **THEN** the system SHALL display a chat bubble containing three animated dots.
- **AND** if the backend sends a status update, the system SHALL display that status text (e.g., "Searching...") alongside or within the animated bubble.
- **AND** the status UI SHALL disappear once the first text chunk of the agent response is received.

### Requirement: File Upload UI and Status
The web interface SHALL provide a file upload button and a visual indicator (File Chip) for the active uploaded file.

#### Scenario: Displaying Uploaded File
- **WHEN** a file is successfully uploaded
- **THEN** a chip displaying the file name and a "remove" button SHALL appear above the chat input.

### Requirement: Supported File Type Communication
The web interface MUST explicitly inform the user that only PDF and Plain Text files are supported.

#### Scenario: Displaying File Requirements
- **WHEN** the user hovers over the upload button or opens the file picker
- **THEN** a hint text or label SHALL display: "Supported: PDF, TXT" or "Please upload a PDF or Text document."

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

### Requirement: Chat History Navigation
The web interface SHALL allow users to browse and select from their list of local chat sessions in the sidebar.

#### Scenario: Selecting a Recent Chat
- **WHEN** a user clicks a chat title in the "Recent Chats" sidebar
- **THEN** the interface SHALL load that specific session's history and set the current persona context accordingly.

## MODIFIED Requirements

### Requirement: Branded Portal Layout
The web interface SHALL use a modern component-based layout (Angular) to implement a high-fidelity, responsive design that is clean, professional, and organizationally neutral, adapting its structure based on the user's device.

#### Scenario: Displaying App Branding
- **WHEN** the application loads
- **THEN** it SHALL show the "Stewardship Portal" title and Dove favicon/branding elements, with NO mention of any specific diocese.

#### Scenario: Displaying Responsive Layout
- **WHEN** the application loads
- **THEN** it SHALL detect the screen size and display either a permanent sidebar (desktop) or a collapsible drawer with a top header (mobile).

## ADDED Requirements

### Requirement: Custom Brand Favicon
The web interface SHALL use the Dove icon (consistent with the portal branding) as the site favicon.

#### Scenario: Verifying Favicon
- **WHEN** the application is loaded in a browser tab
- **THEN** the browser SHALL display the Dove icon in the tab and bookmark bar.
