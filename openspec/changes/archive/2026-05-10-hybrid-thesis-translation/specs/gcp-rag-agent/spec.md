## MODIFIED Requirements

### Requirement: Persona-Driven System Instructions
The agent SHALL adjust its tone and content focus based on the user's selected persona (Priest vs. Parishioner vs. Academic / Researcher).

#### Scenario: Tailoring for Academic / Researcher
- **WHEN** the "Academic / Researcher" persona is active
- **THEN** the agent SHALL prioritize deep synthesis, citation accuracy, and academic-to-approachable translation support.

## ADDED Requirements

### Requirement: Multi-Source Context Injection
The agent SHALL support injecting both a session-persistent File URI and RAG Retrieval tools into a single generation request.

#### Scenario: Generating with Hybrid Context
- **WHEN** a `file_uri` is present in the request
- **THEN** the agent SHALL prepend the file parts to the message contents and enable the RAG tools in the configuration.
