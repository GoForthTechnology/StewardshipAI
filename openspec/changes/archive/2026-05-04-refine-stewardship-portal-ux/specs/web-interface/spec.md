## ADDED Requirements

### Requirement: Branded Portal Layout
The web interface SHALL display the branding of the "Catholic Diocese of Wichita" and use a theme consistent with ecclesiastical stewardship (e.g., specific color palette, typography).

#### Scenario: Displaying Diocesan Branding
- **WHEN** the application loads
- **THEN** it SHALL show the "Catholic Diocese of Wichita Stewardship Portal" title and branding elements.

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
