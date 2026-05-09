## ADDED Requirements

### Requirement: Fluid Component Stacking
The system SHALL automatically stack multi-column components vertically on small screens to maintain readability.

#### Scenario: Discovery Grid Stacking
- **WHEN** the discovery grid is viewed on a screen width less than 768px
- **THEN** it SHALL display its action cards in a single vertical column.

### Requirement: Optimized Mobile Spacing
The system SHALL reduce internal padding and margins on mobile devices to maximize available space for chat content.

#### Scenario: Mobile Chat View
- **WHEN** viewing the chat interface on mobile
- **THEN** the system SHALL apply more compact spacing (e.g., smaller gaps between messages and reduced outer container padding) compared to the desktop view.
