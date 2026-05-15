## MODIFIED Requirements

### Requirement: Dynamic Corpus Retrieval Selection
The agent SHALL support a dynamic list of RAG corpora for retrieval, allowing the retrieval tool to be configured per-request.

#### Scenario: Request with Custom Corpus List
- **WHEN** the `generate_response` method is called with a list of corpus IDs
- **THEN** the system SHALL execute retrieval tasks for each specified corpus ID concurrently using asynchronous execution (e.g., `asyncio.gather`).
- **AND** the results from all corpora SHALL be aggregated before context construction.
