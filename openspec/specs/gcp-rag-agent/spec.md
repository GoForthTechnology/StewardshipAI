## ADDED Requirements

### Requirement: GCP RAG Corpus Integration
The system SHALL integrate with the specified GCP Vertex AI RAG corpus to retrieve relevant document segments for grounding.

#### Scenario: Successful Connection to RAG Corpus
- **WHEN** the agent is initialized with a valid RAG corpus path (e.g., provided via environment variable `GCP_RAG_CORPUS`)
- **THEN** it SHALL establish a valid connection to the Vertex AI RAG engine.

### Requirement: Source-Grounded Responses
The agent MUST answer questions using ONLY the information contained in the provided RAG sources.

#### Scenario: Grounded Answer with Citations
- **WHEN** a user asks a question that can be answered by the corpus
- **THEN** the agent SHALL provide a response based solely on the corpus and include citations for every claim.

### Requirement: Strict Source Lockdown
The agent SHALL NOT use outside knowledge or general training data to answer questions.

#### Scenario: Refusing Outside Information
- **WHEN** a user asks a question about a topic not covered in the RAG corpus
- **THEN** the agent SHALL state: "I cannot answer this because the provided sources do not contain this information."

### Requirement: Citation Enforcement
Every claim made in the agent's response MUST be followed by a citation to the specific source(s) used.

#### Scenario: Correct Citation Formatting
- **WHEN** the agent generates a response with multiple claims
- **THEN** each claim SHALL be followed by a reference to the source document or segment used.
