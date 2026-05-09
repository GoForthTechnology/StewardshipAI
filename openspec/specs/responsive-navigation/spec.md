## ADDED Requirements

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
