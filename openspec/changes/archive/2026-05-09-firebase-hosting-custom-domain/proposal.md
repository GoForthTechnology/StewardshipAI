## Why

The current Cloud Run service region (`us-south1`) does not support direct custom domain mapping. To enable the domain `stewardship.goforthtech.org` for the StewardshipAI portal without the significant effort and risk of a regional migration or the high fixed costs of a Global Application Load Balancer, we will use Firebase Hosting as a free and efficient proxy.

## What Changes

- **Infrastructure**: New Terraform resources to configure a Firebase Hosting site, a "catch-all" rewrite rule pointing to the Cloud Run service, and custom domain mapping.
- **Authentication**: Update the Identity Platform/Firebase Auth `authorized_domains` in Terraform to include `stewardship.goforthtech.org`.
- **Environment**: Potential minor updates to environment variables if the base URL needs to be explicitly configured for the frontend.

## Capabilities

### New Capabilities
- `firebase-hosting-proxy`: Configuration of Firebase Hosting as a serverless proxy to Cloud Run, including custom domain SSL management.

### Modified Capabilities
- `user-authentication`: Update authorized domains list to include the new custom domain to ensure OAuth flows function correctly.

## Impact

- **Terraform**: Modifications to `main.tf` and `variables.tf` (if new variables are needed).
- **DNS**: Requirement for the user to add Firebase-provided A records to their domain registrar.
- **User Experience**: The application will be accessible via `stewardship.goforthtech.org` with automatic SSL.
