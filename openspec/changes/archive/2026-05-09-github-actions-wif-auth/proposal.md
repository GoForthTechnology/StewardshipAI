# Proposal: GitHub Actions CI/CD Fix (WIF)

## Goal
Enable secure, keyless authentication for GitHub Actions using Google Cloud Workload Identity Federation (WIF).

## Problem
The current GitHub Actions deployment workflow is failing because it expects WIF configuration (Provider string and Service Account email) which does not yet exist in the GCP project or the repository's secrets.

## Proposed Solution
1.  **Infrastructure as Code**: Add Terraform resources to create a Workload Identity Pool and Provider specifically for GitHub.
2.  **IAM Lockdown**: Grant the `roles/iam.workloadIdentityUser` role to the GitHub Actions principal set, restricted to the `GoForthTechnology/StewardshipAI` repository. This allows the CI/CD pipeline to safely impersonate the `stewardship-ai-ui-sa` service account.
3.  **Secrets Management**: Provide a clear list of the required secrets to be set in the GitHub repository.

## Scope
- `terraform/main.tf`: Add WIF resources and IAM bindings.
- `terraform/outputs.tf`: Add an output for the `WIF_PROVIDER` string to simplify secret configuration.
- `README.md`: Update with instructions on how to set up the GitHub secrets.

## Risks
- **Repository Visibility**: If the repository was moved or renamed, the WIF IAM binding would need to be updated.
- **Propagation**: WIF changes usually take a few minutes to propagate across GCP.
