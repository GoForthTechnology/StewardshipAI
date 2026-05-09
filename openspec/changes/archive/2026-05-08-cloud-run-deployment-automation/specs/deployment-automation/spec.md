## ADDED Requirements

### Requirement: Artifact Registry Repository
The system SHALL utilize a dedicated Google Artifact Registry repository for storing the project's Docker images.

#### Scenario: Provisioning the First Repository
- **WHEN** the Terraform configuration is applied for the first time
- **THEN** it SHALL create a new Docker repository in Artifact Registry.

### Requirement: Automated Build Pruning
The system SHALL implement a cleanup policy in Artifact Registry to prevent the accumulation of excessive old image versions.

#### Scenario: Image Retention Policy
- **WHEN** a new image is pushed to the repository
- **THEN** the Artifact Registry SHALL automatically prune old images based on a defined policy (e.g., keep last 5 versions or images newer than 30 days).

### Requirement: Orchestrated Manual Deployment
The system SHALL provide a script to orchestrate the build, push, and infrastructure update process for manual deployments.

#### Scenario: Running deploy_manual.sh
- **WHEN** the `deploy_manual.sh` script is executed
- **THEN** it SHALL build the container, push it to Artifact Registry, and apply the Terraform configuration using local environment variables.

### Requirement: GitHub Actions Deployment Pipeline
The system SHALL support an automated CI/CD pipeline using GitHub Actions to deploy changes upon push to the main branch.

#### Scenario: Triggering Automated Deploy
- **WHEN** a change is merged into the `main` branch
- **THEN** the GitHub Action SHALL authenticate with GCP, build/push the image, and trigger a Cloud Run service update.
