## Context

The StewardshipAI project is deployed in `us-south1`, a GCP region that does not yet support direct Cloud Run domain mapping. The application needs to be accessible via `stewardship.goforthtech.org`. We are currently using Firebase Authentication (Identity Platform) which requires authorized domains to be configured for OAuth redirects.

## Goals / Non-Goals

**Goals:**
- Map `stewardship.goforthtech.org` to the Cloud Run service using Firebase Hosting.
- Automate the infrastructure setup via Terraform.
- Ensure Google SSO works correctly on the new custom domain.
- Maintain zero fixed monthly costs for domain mapping.

**Non-Goals:**
- Migrating the Cloud Run service or RAG data to another region.
- Setting up a Global External Application Load Balancer.
- Modifying the frontend application logic (except for environment variables if necessary).

## Decisions

### Decision 1: Use Firebase Hosting as a Serverless Proxy
- **Rationale**: Firebase Hosting provides a free, easy-to-configure proxy to Cloud Run with automatic SSL management. It bypasses the regional limitations of `us-south1`.
- **Alternatives Considered**:
  - **Global Load Balancer**: Rejected due to ~$18/month fixed cost.
  - **Regional Migration**: Rejected due to high effort of re-indexing RAG data in a new region.

### Decision 2: Manage Hosting and Auth Domains via Terraform
- **Rationale**: Keeps the infrastructure as code, ensuring reproducibility and consistency with the existing GCP project setup.
- **Implementation**: Use `google_firebase_hosting_site`, `google_firebase_hosting_version`, and `google_firebase_hosting_custom_domain` resources.

## Risks / Trade-offs

- **[Risk] DNS Propagation Delay** → **Mitigation**: Advise the user that SSL provisioning and DNS propagation can take up to 24 hours.
- **[Risk] Cold Start Latency** → **Mitigation**: Firebase Hosting adds a tiny overhead, but the main latency is still the Cloud Run cold start (if applicable). This is acceptable for this application.
- **[Risk] Auth Domain Mismatch** → **Mitigation**: Ensure `stewardship.goforthtech.org` is added to `google_identity_platform_config` authorized domains in the same Terraform apply.
