## ADDED Requirements

### Requirement: Document Translation with Analogies
The RAG agent SHALL incorporate the uploaded document text as the primary context while utilizing the RAG corpora as secondary reference.

#### Scenario: Complex Text Translation
- **WHEN** a user asks to "revise this text" with a document attached
- **THEN** the agent SHALL prioritize the document's content and retrieve analogies from the RAG corpora to modernize the language.

### Requirement: Document Translator Instruction Set
The system SHALL provide a specialized `RESEARCHER_INSTRUCTION` that focuses on academic-to-approachable translation for various document types.

#### Scenario: Activating Translator Mode
- **WHEN** the "Academic / Researcher" persona is selected
- **THEN** the agent SHALL include instructions to simplify academic syntax and use pastoral analogies in its response generation.
