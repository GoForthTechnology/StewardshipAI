## ADDED Requirements

### Requirement: User Identity Propagation
The system SHALL capture the authenticated user's email address and include it in all requests to the RAG agent.

#### Scenario: User Identity in RAG Request
- **WHEN** an authenticated user (e.g., "dev@company.com") sends a prompt to the agent
- **THEN** the system SHALL include the user's email in the metadata or context passed to the generative model.

### Requirement: Interaction Audit Trails
The system SHALL log each interaction between a user and the research agent, including the user identity, prompt, and timestamp.

#### Scenario: Auditing Interaction
- **WHEN** a response is generated for a user
- **THEN** an audit log entry SHALL be created with the user's email, the query, and the timestamp.
