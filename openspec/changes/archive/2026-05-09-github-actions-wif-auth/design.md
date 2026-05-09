# Design: GitHub Actions CI/CD Fix (WIF)

## Architecture

```ascii
      AUTHENTICATION FLOW
      ════════════════════════════════════════════

      [ GitHub Actions Runner ]
                │
                │ (OIDC Token)
                ▼
      ┌─────────────────────────┐
      │ Google Cloud IAM        │
      ├─────────────────────────┤
      │ [ WIF Pool/Provider ]   │ ◀── Validates Repo Path
      └─────────┬───────────────┘
                │
                │ (Impersonation)
                ▼
      ┌─────────────────────────┐
      │ Service Account (UI SA) │
      ├─────────────────────────┤
      │ [ Project Permissions ] │ ◀── Can Push to GAR & Deploy
      └─────────────────────────┘
```

## Implementation Details

### 1. Terraform Resources

- `google_iam_workload_identity_pool`: Create `github-actions-pool`.
- `google_iam_workload_identity_pool_provider`: Create `github-provider` with `oidc` issuer set to `https://token.actions.githubusercontent.com`.
- `google_service_account_iam_member`: Bind `principalSet` of the repo to the UI service account.

### 2. Output
Add `wif_provider_name` to `outputs.tf` using the format:
`projects/${data.google_project.project.number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_pool.workload_identity_pool_id}/providers/${google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id}`

## Security Considerations
The IAM binding is restricted to:
`principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/GoForthTechnology/StewardshipAI`

This ensures that only actions running in *this* repository can impersonate the service account.
