## ADDED Requirements

### Requirement: Google SSO Authentication
The system SHALL require users to sign in using their Google account via Firebase Authentication before accessing the agent.

#### Scenario: Unauthorized Access Attempt
- **WHEN** an unauthenticated user attempts to access the web UI
- **THEN** the system SHALL redirect them to the Google Sign-In page.

### Requirement: Email Allow-List Enforcement
The system SHALL only allow access to users whose email addresses are present in the authorized allow-list.

#### Scenario: Blocked Unauthorized User
- **WHEN** a user signs in with a Google account NOT in the allow-list
- **THEN** the system SHALL display an "Access Denied" message and prevent interaction with the RAG agent.
