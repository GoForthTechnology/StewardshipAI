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

### Requirement: Automated Traceability for Magisterium Logic
The system SHALL have automated unit tests that verify the retrieval routing and doctrinal grounding logic for all Magisterium-related scenarios.

#### Scenario: Retrieval Routing Verification
- **WHEN** a query is marked with specific corpora intents
- **THEN** the test SHALL verify that the retrieval tool is called with exactly those corpus IDs.

#### Scenario: Grounding Verification via Mocked Context
- **WHEN** a test provides conflicting information from Magisterium and Stewardship sources
- **THEN** the system SHALL prioritize the Magisterium source for theological claims in its evaluation or response synthesis.

