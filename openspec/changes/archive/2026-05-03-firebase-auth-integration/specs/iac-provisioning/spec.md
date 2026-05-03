## ADDED Requirements

### Requirement: Identity Platform Configuration
The system SHALL provide Terraform configuration to enable and configure Google Cloud Identity Platform (Firebase Auth) in the target project.

#### Scenario: Enabling Identity Platform
- **WHEN** the Terraform configuration is applied
- **THEN** the Identity Platform API SHALL be enabled and configured with Google as a permitted sign-in provider.

### Requirement: Secure Configuration Delivery
The system SHALL expose the Firebase API Key and Auth Domain as environment variables for the Cloud Run service.

#### Scenario: Injecting Firebase Config
- **WHEN** the Cloud Run service is provisioned via Terraform
- **THEN** it SHALL include environment variables for `FIREBASE_API_KEY` and `FIREBASE_AUTH_DOMAIN` derived from the project configuration.
