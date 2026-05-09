## Why

StewardshipAI is currently a local-only project. To make it accessible to users and academics, we need to establish our first production environment on Google Cloud Platform. This change will build the foundational infrastructure for Cloud Run and implement a cost-aware deployment pipeline from day one.

## What Changes

- **Registry Establishment**: Create the project's first Artifact Registry repository for container storage.
- **Storage Cost Management**: Implement automated cleanup policies in Artifact Registry from the start to prevent build-up of old images.
- **Infrastructure-as-Code (IaC) Deployment**: Finalize Terraform configurations to provision the Cloud Run service and map all necessary Firebase environment variables.
- **Manual Deployment Script**: Create a `deploy_manual.sh` orchestrator for the initial manual deployment phase.
- **GitHub Actions Foundation**: Establish the directory structure and initial workflow for future automated deployments.

## Capabilities

### New Capabilities
- `deployment-automation`: Requirements for automated build, push, and deploy cycles, including environment variable mapping and cleanup policies.

### Modified Capabilities
- `iac-provisioning`: Updates to Terraform to include Artifact Registry and enhanced environment configuration.

## Impact

- `terraform/`: New resources for Artifact Registry and expanded Cloud Run environment variables.
- `deploy_manual.sh`: New script for orchestrated manual deployments.
- `.github/workflows/`: New directory for CI/CD pipeline definitions.
- `api.py`: Implicitly impacted by the improved passing of environment variables to the frontend.
