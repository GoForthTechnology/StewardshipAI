## ADDED Requirements

### Requirement: GCP RAG Corpus Integration
The system SHALL integrate with any valid Vertex AI RAG corpus provided through environment-driven configuration, which may include paths provided by IaC output.

#### Scenario: Successful Connection to RAG Corpus
- **WHEN** the agent is initialized with a RAG corpus path provided by the IaC output
- **THEN** it SHALL establish a valid connection to the Vertex AI RAG engine.

### Requirement: Source-Grounded Responses
The agent MUST answer questions using ONLY the information contained in the provided RAG sources.

#### Scenario: Grounded Answer with Citations
- **WHEN** a user asks a question that can be answered by the corpus
- **THEN** the agent SHALL provide a response based solely on the corpus and include citations for every claim.

### Requirement: Strict Source Lockdown
The agent SHALL NOT use outside knowledge or general training data to answer questions.

#### Scenario: Refusing Outside Information with Pastoral Redirect
- **WHEN** a user asks a question about a topic not covered in the RAG corpus
- **THEN** the agent SHALL state a helpful, pastoral refusal message such as: "I'm sorry, but our diocese's official stewardship resources don't cover that specific topic. You may want to reach out to the Office of Stewardship for further guidance."

### Requirement: Citation Enforcement
Every claim made in the agent's response MUST be followed by a citation to the specific source(s) used.

#### Scenario: Correct Citation Formatting
- **WHEN** the agent generates a response with multiple claims
- **THEN** each claim SHALL be followed by a reference to the source document or segment used.

### Requirement: Stewardship Guide Persona
The agent SHALL adopt a "Stewardship Guide" persona that is warm, encouraging, and pastoral in tone.

#### Scenario: Pastoral Tone in Responses
- **WHEN** the agent generates a response
- **THEN** it SHALL use welcoming language and emphasize the spiritual mission of stewardship while adhering to the grounding requirements.

### Requirement: Role-Based Response Tailoring
The agent SHALL adjust its tone and content focus based on the user's selected persona (Priest vs. Parishioner).

#### Scenario: Tailoring for Priests
- **WHEN** the "Priest" persona is active
- **THEN** the agent SHALL focus on leadership, parish administration, and homily inspiration.

#### Scenario: Tailoring for Parishioners
- **WHEN** the "Parishioner" persona is active
- **THEN** the agent SHALL focus on personal spiritual practice and practical ways to get involved in Time, Talent, and Treasure.

### Requirement: Cost-Optimized Context Strategy
The agent SHALL support a conditional pivot between "Managed RAG" and "Long Context" retrieval based on cost and scale constraints.

#### Scenario: Pivot to Long Context on Cost Threshold
- **WHEN** the "Managed RAG" (Spanner-backed) infrastructure exceeds the prototype budget
- **THEN** the system SHALL support an alternative retrieval mode that leverages Gemini's Long Context window (pasting documents directly into the prompt) to minimize "idle" hourly infrastructure costs.

#### Scenario: Scale-Based Retrieval Selection
- **WHEN** the total document knowledge base is small enough to fit within the model's context window (e.g., < 1M tokens)
- **THEN** the agent SHALL prioritize the "Long Context" approach to reduce latency and eliminate RAG database costs.

### Requirement: User-Identified Interaction
The agent SHALL support associating queries with a verified user identity (email) for audit logging and session persistence.

#### Scenario: Logging Authenticated Query
- **WHEN** a query is submitted through the web UI
- **THEN** the agent SHALL receive the user's email address and include it in the interaction logs.
