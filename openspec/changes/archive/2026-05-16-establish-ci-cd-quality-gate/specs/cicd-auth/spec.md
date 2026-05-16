## MODIFIED Requirements

### Requirement: Keyless CI/CD Authentication
The system SHALL use Workload Identity Federation (WIF) to authenticate the CI/CD pipeline with Google Cloud, avoiding the use of long-lived service account keys.

#### Scenario: GitHub Actions Authentication
- **WHEN** the GitHub Actions workflow triggers
- **THEN** it SHALL use its OIDC token to exchange for a temporary Google Cloud access token via the Workload Identity Provider.
- **AND** it SHALL impersonate the authorized service account to perform deployment tasks.

#### Scenario: Verify Stage Before Deploy
- **WHEN** the push event occurs on the `main` branch
- **THEN** the pipeline SHALL execute a `verify` job (Unit Tests + Traceability Audit) before proceeding to the `deploy` job.
- **AND** the `deploy` job SHALL depend on the successful completion of the `verify` job.
