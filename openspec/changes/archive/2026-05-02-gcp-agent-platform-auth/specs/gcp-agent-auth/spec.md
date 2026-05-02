## ADDED Requirements

### Requirement: Environment-Driven Configuration
The system SHALL support configuration of GCP project ID, location, and RAG corpus via environment variables.

#### Scenario: Load configuration from environment
- **WHEN** the environment variables `GCP_PROJECT`, `GCP_LOCATION`, and `GCP_RAG_CORPUS` are set
- **THEN** the system SHALL use these values for agent initialization.

### Requirement: Unified Credential Provider
The system SHALL provide a unified way to obtain credentials, prioritizing platform-native Application Default Credentials (ADC) while supporting API keys and Service Account keys.

#### Scenario: Use ADC by default
- **WHEN** no explicit API key or Service Account key is provided and the environment is authorized via gcloud or a GCP service
- **THEN** the system SHALL successfully authenticate using ADC.

#### Scenario: Use Service Account Key
- **WHEN** the `GOOGLE_APPLICATION_CREDENTIALS` environment variable points to a valid JSON key file
- **THEN** the system SHALL successfully authenticate using that service account.

#### Scenario: Use API Key
- **WHEN** a valid API key is provided (either via environment or constructor) and other credential methods are unavailable
- **THEN** the system SHALL successfully authenticate using the API key.
