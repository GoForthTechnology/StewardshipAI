## ADDED Requirements

### Requirement: Neutral Prototype Identity
The application SHALL identify itself as a generic "Stewardship AI Portal" or "Private Prototype" and MUST NOT display any affiliation with a specific diocese or religious organization by default.

#### Scenario: Displaying Generic Title
- **WHEN** the application loads
- **THEN** it SHALL show "Stewardship AI Portal" as the primary title in the header and login screen.

### Requirement: Generic Styling Token System
The application's style system SHALL use generic, brand-neutral naming for its color palette tokens.

#### Scenario: Using Neutral Color Tokens
- **WHEN** applying styles to UI components
- **THEN** the system SHALL use tokens like `brand-primary`, `brand-background`, and `brand-accent` instead of organization-specific names.
