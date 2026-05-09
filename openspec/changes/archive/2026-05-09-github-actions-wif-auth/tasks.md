# Tasks: GitHub Actions CI/CD Fix (WIF)

## 1. Infrastructure (Terraform)

- [x] 1.1 Add `data "google_project" "project" {}` to `terraform/main.tf` to retrieve the project number.
- [x] 1.2 Add `google_iam_workload_identity_pool` resource to `terraform/main.tf`.
- [x] 1.3 Add `google_iam_workload_identity_pool_provider` resource for GitHub to `terraform/main.tf`.
- [x] 1.4 Add `google_service_account_iam_member` resource to allow repository-based impersonation.
- [x] 1.5 Add `wif_provider_name` output to `terraform/outputs.tf`.

## 2. Configuration & Secrets

- [x] 2.1 Run `terraform apply` to provision the WIF infrastructure.
- [x] 2.2 Retrieve the `wif_provider_name` from Terraform output.
- [x] 2.3 Set the `WIF_PROVIDER` secret in the GitHub repository.
- [x] 2.4 Set the `WIF_SERVICE_ACCOUNT` secret in the GitHub repository (`stewardship-ai-ui-sa@stewardship-ai.iam.gserviceaccount.com`).
- [x] 2.5 Set the `GCP_PROJECT_ID` (`stewardship-ai`) and `GCP_LOCATION` (`us-south1`) secrets in the GitHub repository.

## 3. Verification

- [x] 3.1 Push a dummy change (or this commit) to GitHub.
- [x] 3.2 Verify the "Google Auth" step in GitHub Actions successfully exchanges the OIDC token.
- [x] 3.3 Verify the "Build and Push Container" step successfully authenticates to Artifact Registry.
- [x] 3.4 Verify the "Deploy to Cloud Run" step successfully updates the service.
