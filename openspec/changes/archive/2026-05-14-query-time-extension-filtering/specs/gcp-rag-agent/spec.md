## MODIFIED Requirements

### Requirement: Multi-Source Context Injection
The agent SHALL support injecting both a session-persistent File URI and filtered RAG retrieval results into a single generation request.

#### Scenario: Generating with Synthetic Context
- **WHEN** a query is processed
- **THEN** the agent SHALL prepend any session-persistent file content AND the filtered RAG chunks to the message contents before calling the generative model.
