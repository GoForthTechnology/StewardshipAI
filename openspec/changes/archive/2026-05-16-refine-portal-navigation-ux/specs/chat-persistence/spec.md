## MODIFIED Requirements

### Requirement: Chat Session Titling
The system SHALL support assigning descriptive titles to chat sessions based on the content of the initial exchange, utilizing both local heuristics and remote LLM generation.

#### Scenario: Initializing a Chat Title
- **WHEN** a new chat session is created
- **THEN** the system SHALL initially generate a local title using a word-slice fallback (e.g., the first 4 words of the prompt).

#### Scenario: Refining a Chat Title
- **WHEN** the first turn of a new chat session completes
- **THEN** the system SHALL trigger an asynchronous request to generate a concise, relevant title via LLM.
- **AND** the system SHALL ONLY update the session title if the returned title is non-empty and distinct from the generic "New Chat" placeholder.
