## ADDED Requirements

### Requirement: Frontend Request Timeout
The web interface SHALL implement a client-side timeout for chat generation requests to prevent the UI from appearing hung.

#### Scenario: Frontend Request Timeout
- **WHEN** a chat generation request does not receive a response within 15 seconds
- **THEN** the interface SHALL abort the request and display a specific timeout error message to the user.

### Requirement: Differentiated Error Feedback
The web interface SHALL provide specific visual feedback for different types of request failures.

#### Scenario: Displaying Timeout Error
- **WHEN** a request is aborted due to a timeout
- **THEN** the system SHALL display a message like "The request took too long. Please try again."

#### Scenario: Displaying Generic Error
- **WHEN** a request fails due to any other network or server error
- **THEN** the system SHALL display a message like "I encountered an error connecting to our resources. Please try again later."
