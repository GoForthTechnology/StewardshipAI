## MODIFIED Requirements

### Requirement: Google SSO Authentication
The system SHALL require users to sign in using their Google account via Firebase Authentication before accessing the agent.

#### Scenario: Successful Token Verification
- **WHEN** a user signs in via the Google SSO UI
- **THEN** the system SHALL verify the returned ID Token using the Firebase Admin SDK on the backend before granting access.

#### Scenario: Expired or Invalid Token
- **WHEN** a user provides an expired or malformed JWT token
- **THEN** the system SHALL reject the token and redirect the user back to the sign-in flow.
