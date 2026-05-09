## MODIFIED Requirements

### Requirement: Strict Source Lockdown
The agent SHALL NOT use outside knowledge or general training data to answer questions.

#### Scenario: Refusing Outside Information with Pastoral Redirect
- **WHEN** a user asks a question about a topic not covered in the RAG corpus
- **THEN** the agent SHALL state a helpful, pastoral refusal message such as: "I'm sorry, but our official stewardship resources don't cover that specific topic. You may want to reach out to the stewardship office for further guidance."

### Requirement: Anonymized Greetings
The agent SHALL NOT include raw technical identifiers (like email addresses) in its conversational output and SHALL avoid organization-specific preambles.

#### Scenario: Greeting the User
- **WHEN** the agent begins a response
- **THEN** it SHALL provide the requested information immediately without organization-specific greetings or preambles.
