## MODIFIED Requirements

### Requirement: Persona Selection
The web interface SHALL provide a clear mechanism for users to select whether they are interacting as a "Parishioner", a "Priest/Leader", or an "Academic / Researcher".

#### Scenario: Selecting a Persona
- **WHEN** a user selects a persona from the toggle, sidebar buttons, or other selection mechanism
- **THEN** the system SHALL update the session state and pass this context to the RAG agent for subsequent queries.
