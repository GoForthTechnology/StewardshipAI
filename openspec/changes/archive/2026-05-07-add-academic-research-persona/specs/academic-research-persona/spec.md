## ADDED Requirements

### Requirement: Academic Research System Instruction
The RAG agent SHALL utilize a specialized system instruction for the "Academic / Researcher" persona that prioritizes deep analysis, cross-document synthesis, and academic rigor.

#### Scenario: Researcher Persona Instruction Selection
- **WHEN** the "researcher" persona is passed to the RAG agent
- **THEN** the agent SHALL utilize the `RESEARCHER_INSTRUCTION` set.

### Requirement: Citation Requirement for Researchers
The "Academic / Researcher" persona SHALL include explicit citations to the source material in its responses.

#### Scenario: Response with Citations
- **WHEN** the "researcher" persona generates a response
- **THEN** it SHALL include inline or end-of-response citations referencing the specific documents from the RAG corpus.

### Requirement: Theological Synthesis suggested prompts
The system SHALL provide suggested prompts tailored to theological and stewardship research when the Academic persona is active.

#### Scenario: Displaying Research Prompts
- **WHEN** the "researcher" persona is active
- **THEN** the discovery grid SHALL display prompts such as "Synthesize the main theological themes regarding stewardship across the available documents."
