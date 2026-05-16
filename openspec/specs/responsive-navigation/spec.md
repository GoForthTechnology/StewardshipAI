# Responsive Navigation Specification

## Purpose
Define requirements for how the application adapts its navigation and layout across different device sizes.
## Requirements
### Requirement: Responsive Side Drawer
The system SHALL provide a collapsible navigation drawer that is hidden by default on small screens (e.g., width < 768px).

#### Scenario: Opening Drawer on Mobile
- **WHEN** a user on a mobile device taps the hamburger menu icon
- **THEN** the navigation drawer SHALL slide into view, providing access to persona selection and sign-out.

### Requirement: Mobile Brand Header
The system SHALL display a persistent top header on small screens that includes the application branding and a navigation trigger.

#### Scenario: Viewing Mobile Header
- **WHEN** the application is viewed on a device with a screen width less than 768px
- **THEN** it SHALL show a header containing the "🕊️ Portal" title and a menu icon.

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

