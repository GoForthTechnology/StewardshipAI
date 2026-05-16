## MODIFIED Requirements

### Requirement: CI/CD Quality Gate
The CI/CD pipeline SHALL include a dedicated "Verify" stage that executes all unit tests and the traceability audit before the "Deploy" stage.

#### Scenario: Failing Pipeline on Test Failure
- **WHEN** any backend or frontend test fails during the Verify stage
- **THEN** the pipeline SHALL terminate immediately and prevent the deployment to Cloud Run.

#### Scenario: Failing Pipeline on Coverage Regression
- **WHEN** the traceability audit fails during the Verify stage
- **THEN** the pipeline SHALL terminate and prevent deployment, even if all other tests pass.

#### Scenario: Clean Environment Verification
- **WHEN** the `verify` job executes in CI
- **THEN** it SHALL NOT depend on secret environment variables for agent initialization.
- **AND** it SHALL verify that the test suite provides its own isolated configuration.
