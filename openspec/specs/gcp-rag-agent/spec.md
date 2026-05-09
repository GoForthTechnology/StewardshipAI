## ADDED Requirements

### Requirement: GCP RAG Corpus Integration
The system SHALL integrate with any valid Vertex AI RAG corpus provided through environment-driven configuration, which may include paths provided by IaC output.

#### Scenario: Successful Connection to RAG Corpus
- **WHEN** the agent is initialized with a RAG corpus path provided by the IaC output
- **THEN** it SHALL establish a valid connection to the Vertex AI RAG engine.

### Requirement: Source-Grounded Responses
The agent MUST answer questions using ONLY the information contained in the provided RAG sources.

#### Scenario: Grounded Answer without Citations
- **WHEN** a user asks a question that can be answered by the corpus
- **THEN** the agent SHALL provide a response based solely on the corpus and SHALL NOT include explicit citations.

### Requirement: Strict Source Lockdown
The agent SHALL NOT use outside knowledge or general training data to answer questions.

#### Scenario: Refusing Outside Information with Pastoral Redirect
- **WHEN** a user asks a question about a topic not covered in the RAG corpus
- **THEN** the agent SHALL state a helpful, pastoral refusal message such as: "I'm sorry, but our diocese's official stewardship resources don't cover that specific topic. You may want to reach out to the Office of Stewardship for further guidance."

### Requirement: Stewardship Guide Persona
The agent SHALL adopt a "Stewardship Guide" persona that is professional, concise, and pastoral in tone.

#### Scenario: Professional Tone in Responses
- **WHEN** the agent generates a response
- **THEN** it SHALL use direct language that emphasizes the spiritual mission of stewardship while avoiding overly flowery preamble (e.g., "It's wonderful to talk about...") or repetitive encouragement.

#### Scenario: Conversational Tone in Responses
- **WHEN** the agent generates a response
- **THEN** it SHALL use welcoming, conversational language and weave information from the documents naturally into the dialogue without structured evidence markers or citations.

### Requirement: Role-Based Response Tailoring
The agent SHALL adjust its tone and content focus based on the user's selected persona (Priest vs. Parishioner vs. Academic / Researcher).

#### Scenario: Tailoring for Priests
- **WHEN** the "Priest" persona is active
- **THEN** the agent SHALL focus on leadership, parish administration, and homily inspiration.

#### Scenario: Tailoring for Parishioners
- **WHEN** the "Parishioner" persona is active
- **THEN** the agent SHALL focus on personal spiritual practice and practical ways to get involved in Time, Talent, and Treasure.

#### Scenario: Tailoring for Academic / Researcher
- **WHEN** the "researcher" persona is active
- **THEN** the agent SHALL focus on deep theological analysis, synthesis across multiple documents, and academic writing support.

### Requirement: Cost-Optimized Context Strategy
The agent SHALL support a conditional pivot between "Managed RAG" and "Long Context" retrieval based on cost and scale constraints.

#### Scenario: Pivot to Long Context on Cost Threshold
- **WHEN** the "Managed RAG" (Spanner-backed) infrastructure exceeds the prototype budget
- **THEN** the system SHALL support an alternative retrieval mode that leverages Gemini's Long Context window (pasting documents directly into the prompt) to minimize "idle" hourly infrastructure costs.

#### Scenario: Scale-Based Retrieval Selection
- **WHEN** the total document knowledge base is small enough to fit within the model's context window (e.g., < 1M tokens)
- **THEN** the agent SHALL prioritize the "Long Context" approach to reduce latency and eliminate RAG database costs.

### Requirement: User-Identified Interaction
The agent SHALL support associating queries with a verified user identity (email) and conversational context (history) for audit logging and contextual response generation.

#### Scenario: Generating Response with History
- **WHEN** a query is submitted with an associated history of previous messages
- **THEN** the agent SHALL utilize both the history and the RAG corpus to generate a contextually relevant response asynchronously.
- **AND** the interaction log SHALL include the context of the multi-turn interaction.

#### Scenario: Logging Authenticated Query
- **WHEN** a query is submitted through the web UI
- **THEN** the agent SHALL receive the user's email address and include it in the interaction logs.

### Requirement: Structured Markdown Output
The agent SHALL output responses using structured markdown with mandatory spacing for readability.

#### Scenario: Readable List Formatting
- **WHEN** the agent generates a list (bulleted or numbered)
- **THEN** it SHALL include a double newline between each list item and before/after the list block.

### Requirement: Anonymized Greetings
The agent SHALL NOT include raw technical identifiers (like email addresses) in its conversational output.

#### Scenario: Greeting the User
- **WHEN** the agent begins a response
- **THEN** it SHALL refer to the user by their role (e.g., "Dear Parishioner") or use a general greeting (e.g., "Welcome") instead of the user's email address.

### Requirement: RAG Parameter Type Safety
The agent SHALL enforce strict type validation for the RAG corpus name to prevent configuration errors.

#### Scenario: Robust Parameter Handling
- **WHEN** the agent configuration is generated
- **THEN** the system SHALL utilize keyword arguments for all internal method calls.
- **AND** the system SHALL explicitly verify that the corpus name is a string before passing it to the underlying SDK.
