## ADDED Requirements

### Requirement: Multi-Corpus Retrieval
The system SHALL support simultaneous retrieval from multiple Vertex AI RAG corpora to provide layered context (local vs. universal).

#### Scenario: Querying with Dual Corpora
- **WHEN** a user submits a query to the agent
- **THEN** the system SHALL invoke the retrieval tool using both the `Stewardship Corpus` and the `Magisterium Corpus`.
- **AND** the system SHALL combine relevant chunks from both sources into the context provided to the generative model.

### Requirement: Theological-Practical Synthesis
The system SHALL synthesize responses that prioritize universal Church doctrine for theological questions while using local resources for practical stewardship advice.

#### Scenario: Synthesis of Universal Doctrine
- **WHEN** a user asks a question with moral or theological implications (e.g., "What is the dignity of work in the context of AI?")
- **THEN** the agent SHALL ground its primary response in documents from the `Magisterium Corpus`.

#### Scenario: Local Application of Doctrine
- **WHEN** a user asks for practical stewardship advice (e.g., "How do I start a tithing plan?")
- **THEN** the agent SHALL ground its primary response in documents from the `Stewardship Corpus`, ensuring the advice is consistent with the `Magisterium Corpus`.
