# magisterium-retrieval Specification

## Purpose
Enable simultaneous retrieval from multiple Vertex AI RAG corpora to provide layered theological and practical context.
## Requirements
### Requirement: Multi-Corpus Retrieval
The system SHALL support retrieval from one or more Vertex AI RAG corpora as specified by the user's selection.

#### Scenario: Querying with Selected Corpora
- **WHEN** a user submits a query to the agent with specific corpora selected
- **THEN** the system SHALL invoke the retrieval tool using only the selected corpora.
- **AND** the system SHALL combine relevant chunks from all selected sources into the context provided to the generative model.

### Requirement: Theological-Practical Synthesis
The system SHALL synthesize responses that prioritize universal Church doctrine for theological questions while using local resources for practical stewardship advice.

#### Scenario: Synthesis of Universal Doctrine
- **WHEN** a user asks a question with moral or theological implications (e.g., "What is the dignity of work in the context of AI?")
- **THEN** the agent SHALL ground its primary response in documents from the `Magisterium Corpus`.

#### Scenario: Local Application of Doctrine
- **WHEN** a user asks for practical stewardship advice (e.g., "How do I start a tithing plan?")
- **THEN** the agent SHALL ground its primary response in documents from the `Stewardship Corpus`, ensuring the advice is consistent with the `Magisterium Corpus`.

