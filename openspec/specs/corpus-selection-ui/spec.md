# corpus-selection-ui Specification

## Purpose
TBD - created by archiving change multi-corpus-selection. Update Purpose after archive.
## Requirements
### Requirement: Corpus Selection Controls
The system SHALL provide a user interface for selecting which RAG corpora are used for grounding the agent's responses.

#### Scenario: Viewing available corpora
- **WHEN** the user opens the portal sidebar
- **THEN** the system SHALL display a list of all available RAG corpora (e.g., "Stewardship Resources", "Universal Magisterium") with toggle switches.

#### Scenario: Toggling a corpus
- **WHEN** the user toggles a corpus switch
- **THEN** the system SHALL update the active selection state.

### Requirement: Mandatory Corpus Selection
The system SHALL ensure that at least one RAG corpus is selected before allowing a chat request to be sent.

#### Scenario: Disabling last corpus
- **WHEN** the user attempts to disable the only remaining active corpus
- **THEN** the system SHALL prevent the deactivation and display a message stating that at least one resource must be selected.

