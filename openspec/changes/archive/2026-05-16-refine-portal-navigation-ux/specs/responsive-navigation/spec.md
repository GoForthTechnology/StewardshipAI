## ADDED Requirements

### Requirement: Header Persona Switcher
The system SHALL display the persona selection mechanism in the chat header, allowing users to switch roles while viewing their active conversation.

#### Scenario: Switching Persona on Desktop
- **WHEN** an authenticated user on a desktop device clicks a persona button in the header
- **THEN** the system SHALL update the active persona for the current session.
- **AND** the system SHALL visually highlight the newly active persona.

#### Scenario: Switching Persona on Mobile
- **WHEN** an authenticated user on a mobile device interacts with the persona switcher in the header
- **THEN** the system SHALL display a condensed selection mechanism (e.g., a dropdown or modal).
- **AND** update the active persona upon selection.
