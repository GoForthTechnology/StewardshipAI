## ADDED Requirements

### Requirement: Keyless CI/CD Authentication
The system SHALL use Workload Identity Federation (WIF) to authenticate the CI/CD pipeline with Google Cloud, avoiding the use of long-lived service account keys.

#### Scenario: GitHub Actions Authentication
- **WHEN** the GitHub Actions workflow triggers
- **THEN** it SHALL use its OIDC token to exchange for a temporary Google Cloud access token via the Workload Identity Provider.
- **AND** it SHALL impersonate the authorized service account to perform deployment tasks.

### Requirement: Repository-Restricted Impersonation
The CI/CD impersonation SHALL be strictly limited to the specific GitHub repository owning the project.

#### Scenario: unauthorized Impersonation Blocked
- **WHEN** an action from a DIFFERENT repository attempts to use the Workload Identity Pool
- **THEN** Google Cloud IAM SHALL reject the request.
