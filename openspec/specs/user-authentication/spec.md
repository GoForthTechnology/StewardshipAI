## ADDED Requirements

### Requirement: Google SSO Authentication
The system SHALL require users to sign in using their Google account via Firebase Authentication (client-side) before accessing the agent API.

#### Scenario: Unauthorized Access Attempt
- **WHEN** an unauthenticated user attempts to access the Angular web UI
- **THEN** the system SHALL present the Google Sign-In page.

#### Scenario: Successful Token Verification
- **WHEN** a user signs in via the Google SSO UI
- **THEN** the Angular client SHALL obtain a Firebase ID Token and send it to the FastAPI backend, which SHALL verify it using the Firebase Admin SDK before granting access.

#### Scenario: Expired or Invalid Token
- **WHEN** a user provides an expired or malformed JWT token to the backend
- **THEN** the backend SHALL reject the token (401), and the frontend SHALL redirect the user back to the sign-in flow.

### Requirement: Email Allow-List Enforcement
The system SHALL only allow access to users whose email addresses are present in the authorized allow-list.

#### Scenario: Blocked Unauthorized User
- **WHEN** a user signs in with a Google account NOT in the allow-list
- **THEN** the system SHALL display an "Access Denied" message and prevent interaction with the RAG agent.

### Requirement: Authorized Domain for OAuth
The custom domain `stewardship.goforthtech.org` MUST be added to the list of authorized domains for Identity Platform to allow OAuth redirects.

#### Scenario: Successful Redirect from Custom Domain
- **WHEN** a user initiates Google SSO from `https://stewardship.goforthtech.org`
- **THEN** the Identity Platform SHALL permit the OAuth redirect back to the custom domain upon successful authentication.
