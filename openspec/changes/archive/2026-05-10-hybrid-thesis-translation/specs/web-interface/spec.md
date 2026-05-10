## MODIFIED Requirements

### Requirement: Persona Selection and Display
The web interface SHALL provide a clear mechanism for users to select whether they are interacting as a "Parishioner", a "Priest/Leader", or an "Academic / Researcher".

#### Scenario: Switching Personas
- **WHEN** user selects a new persona from the navigation
- **THEN** the interface SHALL update the active persona indicator and adjust the suggested prompts in the Discovery Grid.

### Requirement: Application Title and Header
The web interface SHALL display the application title "Stewardship Portal" in the header and document title.

#### Scenario: Header Title Display
- **WHEN** the application loads
- **THEN** the header SHALL show "Stewardship Portal" with the Dove icon.

## ADDED Requirements

### Requirement: File Upload UI and Status
The web interface SHALL provide a file upload button and a visual indicator (File Chip) for the active uploaded file.

#### Scenario: Displaying Uploaded File
- **WHEN** a file is successfully uploaded
- **THEN** a chip displaying the file name and a "remove" button SHALL appear above the chat input.

### Requirement: Supported File Type Communication
The web interface MUST explicitly inform the user that only PDF and Plain Text files are supported.

#### Scenario: Displaying File Requirements
- **WHEN** the user hovers over the upload button or opens the file picker
- **THEN** a hint text or label SHALL display: "Supported: PDF, TXT" or "Please upload a PDF or Text document."
