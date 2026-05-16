## ADDED Requirements

### Requirement: Automated Traceability for Magisterium Logic
The system SHALL have automated unit tests that verify the retrieval routing and doctrinal grounding logic for all Magisterium-related scenarios.

#### Scenario: Retrieval Routing Verification
- **WHEN** a query is marked with specific corpora intents
- **THEN** the test SHALL verify that the retrieval tool is called with exactly those corpus IDs.

#### Scenario: Grounding Verification via Mocked Context
- **WHEN** a test provides conflicting information from Magisterium and Stewardship sources
- **THEN** the system SHALL prioritize the Magisterium source for theological claims in its evaluation or response synthesis.
