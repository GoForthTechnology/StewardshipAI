## ADDED Requirements

### Requirement: Animated Request Pending State
The web interface SHALL display an animated ellipsis ("...") visual feedback when a message has been sent and is awaiting a response from the agent.

#### Scenario: Visual Feedback for Pending Message
- **WHEN** a user submits a query
- **THEN** the system SHALL display a chat bubble containing three animated dots that bounce or pulse to indicate the request is being processed.
- **AND** the animated bubble SHALL disappear once the first chunk of the agent response is received.