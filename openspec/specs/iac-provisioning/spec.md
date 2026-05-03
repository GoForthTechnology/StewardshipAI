## ADDED Requirements

### Requirement: Terraform-Based Provisioning
The system SHALL provide Terraform configuration files to provision a Vertex AI RAG corpus.

#### Scenario: Provisioning RAG Corpus
- **WHEN** the Terraform configuration is applied with valid GCP credentials
- **THEN** a new Vertex AI RAG corpus SHALL be created in the specified GCP project and location.

### Requirement: Externalized Resource Configuration
The system SHALL expose the RAG corpus ID as a Terraform output.

#### Scenario: Accessing Corpus ID
- **WHEN** the Terraform provisioning is complete
- **THEN** the system SHALL provide the full resource ID of the newly created RAG corpus as an output.

### Requirement: GCS Bucket Integration & IAM Permissions
The system SHALL support connecting the RAG corpus to a GCS bucket and grant the necessary IAM permissions to the RAG Service Agent.

#### Scenario: Granting Read Access to RAG Service Agent
- **WHEN** the Terraform configuration is applied with a specified GCS bucket name
- **THEN** it SHALL grant the `roles/storage.objectViewer` role to the Vertex AI RAG Service Agent on that bucket.

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
