## MODIFIED Requirements

### Requirement: Multi-Corpus Retrieval
The system SHALL support retrieval from one or more Vertex AI RAG corpora as specified by the user's selection.

#### Scenario: Querying with Selected Corpora
- **WHEN** a user submits a query to the agent with specific corpora selected
- **THEN** the system SHALL invoke the retrieval tool using only the selected corpora.
- **AND** the system SHALL combine relevant chunks from all selected sources into the context provided to the generative model.
