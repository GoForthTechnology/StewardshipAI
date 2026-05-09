## Context

The application is currently running locally via Docker. We are establishing the first GCP production environment using Artifact Registry and Cloud Run.

## Goals / Non-Goals

**Goals:**
- Establish the first Artifact Registry repository for the project.
- Automate registry cleanup to control costs from day one.
- Deploy the first Cloud Run service instance with full Firebase configuration.
- Provide a clear, repeatable manual deployment path before moving to CI/CD.

**Non-Goals:**
- Supporting multiple environments (dev/prod) in this initial push (single prod environment only).
- Migrating legacy images.

## Decisions

### 1. Artifact Registry Cleanup
**Decision**: Use Terraform `google_artifact_registry_repository` with a `cleanup_policies` block.
**Rationale**: Native GCP solution for managing image bloat. We will keep the last 5 tagged versions.

### 2. Manual Deployment Wrapper
**Decision**: Create `deploy_manual.sh` that sources `setup_env.sh`, runs `gcloud builds submit`, and `terraform apply`. Includes a `--skip-build` optimization flag.
**Rationale**: Leverages existing patterns while reducing human error during multi-step deployments.

### 3. Terraform Variable Expansion
**Decision**: Add all missing Firebase fields (Storage Bucket, App ID, etc.) and Google OAuth credentials to `variables.tf` and inject them into the Cloud Run container.
**Rationale**: Essential for frontend authentication and service functionality in production.

### 4. Provider & Authentication (Troubleshooting)
**Decision**: Use `google-beta` provider and set `user_project_override = true` and `billing_project` in the provider configuration.
**Rationale**: Critical to resolve 403 Quota errors when using local Application Default Credentials (ADC) with Identity Platform during Terraform operations.

### 5. RAG Resource Management (Divergence)
**Decision**: Remove Vertex AI RAG Corpus and Engine resources from Terraform.
**Rationale**: Inconsistent Terraform provider support for RAG resources. These are managed manually/via gcloud, with the ID passed into Cloud Run via environment variables.

## Risks / Trade-offs

- **[Risk] Cleanup Policy deletes critical image** → **Mitigation**: Use "KEEP" actions for tagged images and only prune older, untagged, or excessive versions.
- **[Risk] Local env mismatch with Terraform** → **Mitigation**: The `deploy_manual.sh` script will explicitly generate a `.tfvars` file from the current shell environment to ensure parity.
