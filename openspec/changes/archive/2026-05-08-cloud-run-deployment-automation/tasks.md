## 1. Infrastructure (Terraform)

- [x] 1.1 Add `google_artifact_registry_repository` resource to `terraform/main.tf`
- [x] 1.2 Implement `cleanup_policies` in Artifact Registry to retain only the last 5 images
- [x] 1.3 Update `terraform/variables.tf` to include all Firebase config fields (Storage Bucket, App ID, etc.)
- [x] 1.4 Map all Firebase variables into the `google_cloud_run_v2_service` environment block in `main.tf`

## 2. Automation Scripts

- [x] 2.1 Create `deploy_manual.sh` at the project root
- [x] 2.2 Implement logic in `deploy_manual.sh` to source `setup_env.sh`, build with `gcloud builds`, and generate `terraform.tfvars`
- [x] 2.3 Add a "Plan before Apply" confirmation step to the manual deploy script

## 3. GitHub Actions Foundation

- [x] 3.1 Create `.github/workflows/deploy.yml` with the basic structure for building and pushing the image
- [x] 3.2 Document the required GitHub Secrets in the workflow comments

## 4. Verification

- [ ] 4.1 Run `deploy_manual.sh` and verify the container is built and pushed to Artifact Registry
- [ ] 4.2 Confirm that the Cloud Run service is updated and correctly receives the expanded Firebase configuration
- [ ] 4.3 Manually trigger a cleanup or verify the policy is active in the GCP console
