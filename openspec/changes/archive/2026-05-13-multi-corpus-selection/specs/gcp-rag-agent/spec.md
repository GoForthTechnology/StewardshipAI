## ADDED Requirements

### Requirement: Dynamic Corpus Retrieval Selection
The agent SHALL support a dynamic list of RAG corpora for retrieval, allowing the retrieval tool to be configured per-request.

#### Scenario: Request with Custom Corpus List
- **WHEN** the `generate_response` method is called with a list of corpus IDs
- **THEN** the system SHALL create one retrieval tool for each specified corpus ID in the `GenerateContentConfig`.
