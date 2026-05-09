## 1. Terraform Infrastructure

- [x] 1.1 Add `firebasehosting.googleapis.com` to project services in `main.tf`.
- [x] 1.2 Add `google_firebase_hosting_site` resource for `stewardship-portal`.
- [x] 1.3 Add `google_firebase_hosting_version` with catch-all rewrite to Cloud Run service.
- [x] 1.4 Add `google_firebase_hosting_custom_domain` for `stewardship.goforthtech.org`.
- [x] 1.5 Update `google_identity_platform_config.default` authorized domains to include the custom domain.

## 2. Validation & Deployment

- [x] 2.1 Run `terraform plan` to verify the changes.
- [x] 2.2 Run `terraform apply` to provision the resources.
- [x] 2.3 Provide the generated A records to the user for DNS configuration.
- [x] 2.4 Verify that `https://stewardship.goforthtech.org` redirects to Cloud Run after DNS propagation.
- [x] 2.5 Verify that Google SSO works on the custom domain.
