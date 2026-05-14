## ADDED Requirements

### Requirement: Nested Extension Selection
The system SHALL allow users to select specific file extensions to include in the query for each active corpus.

#### Scenario: Expanding a corpus for extension filtering
- **WHEN** the user is in the portal sidebar
- **THEN** the system SHALL display extension filters (PDF, Word, TXT, Other) as nested options under each enabled corpus.

### Requirement: Default Extension State
The system SHALL default all extension filters to "enabled" for any newly active corpus.

#### Scenario: Initializing extensions
- **WHEN** the portal loads
- **THEN** all corpora SHALL have all extension filters (PDF, Word, TXT, Other) enabled by default.

### Requirement: Persistence of Extension Selection
The system SHALL preserve the user's extension selection across the session.

#### Scenario: Changing persona
- **WHEN** the user changes their persona (e.g., from Parishioner to Priest)
- **THEN** the selected extension filters for each corpus SHALL remain unchanged.
