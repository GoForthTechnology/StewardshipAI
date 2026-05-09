## MODIFIED Requirements

### Requirement: Secure Configuration Delivery
The system SHALL expose the full Firebase configuration (API Key, Auth Domain, Storage Bucket, etc.) as environment variables for the Cloud Run service.

#### Scenario: Injecting Firebase Config
- **WHEN** the Cloud Run service is provisioned via Terraform
- **THEN** it SHALL include environment variables for `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_STORAGE_BUCKET`, `FIREBASE_APP_ID`, and other required Firebase fields derived from the project configuration.
