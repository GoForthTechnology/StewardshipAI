## ADDED Requirements

### Requirement: Session-Persistent Document Upload
The system SHALL provide an endpoint to upload a PDF or text file that persists within the active GenAI session.

#### Scenario: Successful Document Upload
- **WHEN** a user uploads a valid PDF or .txt file under 10MB
- **THEN** the system SHALL extract the text and return a unique file reference URI.

### Requirement: File Safeguards and Validation
The system MUST enforce strict limits on file size and type to protect against resource exhaustion.

#### Scenario: Reject Over-Sized File
- **WHEN** a user attempts to upload a file larger than 10MB
- **THEN** the system SHALL reject the upload with an error message.

### Requirement: Backend Text Extraction
The system SHALL automatically extract text from uploaded PDF documents to ensure compatibility with grounding tools.

#### Scenario: PDF Text Extraction
- **WHEN** a PDF is uploaded
- **THEN** the system SHALL use a parsing library (pypdf) to convert the content into a text string before passing it to the agent.
