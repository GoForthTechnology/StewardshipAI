## MODIFIED Requirements

### Requirement: Persona Selection and Display
The web interface SHALL provide a clear mechanism for users to select whether they are interacting as a "Parishioner", a "Priest/Leader", or an "Academic / Researcher" located in the chat header.

#### Scenario: Selecting a Persona
- **WHEN** a user selects a persona from the header switcher
- **THEN** the system SHALL update the session state and pass this context to the RAG agent for subsequent queries.

#### Scenario: Switching Personas
- **WHEN** user selects a new persona from the header navigation
- **THEN** the interface SHALL update the active persona indicator and adjust the suggested prompts in the Discovery Grid.

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
- **AND** technical extension filters in the sidebar SHALL only be visible when the "Academic / Researcher" persona is active.
