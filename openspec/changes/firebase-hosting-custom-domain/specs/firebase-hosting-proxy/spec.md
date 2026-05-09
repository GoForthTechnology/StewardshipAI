## ADDED Requirements

### Requirement: Firebase Hosting Proxy to Cloud Run
The system SHALL use Firebase Hosting to proxy all incoming traffic to the Cloud Run service.

#### Scenario: Catch-all Routing
- **WHEN** a request is made to `stewardship.goforthtech.org/*`
- **THEN** Firebase Hosting SHALL rewrite the request to the target Cloud Run service in `us-south1`.

### Requirement: Custom Domain SSL
The system SHALL provide an automatically provisioned and managed SSL certificate for the custom domain.

#### Scenario: Secure Access
- **WHEN** a user navigates to `https://stewardship.goforthtech.org`
- **THEN** the browser SHALL establish a secure connection using a valid certificate.
