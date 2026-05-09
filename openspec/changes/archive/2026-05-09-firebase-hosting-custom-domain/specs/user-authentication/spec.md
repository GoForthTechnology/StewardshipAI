## ADDED Requirements

### Requirement: Authorized Domain for OAuth
The custom domain `stewardship.goforthtech.org` MUST be added to the list of authorized domains for Identity Platform to allow OAuth redirects.

#### Scenario: Successful Redirect from Custom Domain
- **WHEN** a user initiates Google SSO from `https://stewardship.goforthtech.org`
- **THEN** the Identity Platform SHALL permit the OAuth redirect back to the custom domain upon successful authentication.
