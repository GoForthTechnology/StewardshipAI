## ADDED Requirements

### Requirement: Deterministic Mocking Strategy
The system's automated tests SHALL use a deterministic mocking strategy for asynchronous operations, specifically for streaming and generator-based responses.

#### Scenario: Async Stream Mocking
- **WHEN** mocking an asynchronous stream (e.g., Vertex AI response)
- **THEN** the mock SHALL correctly implement the `__aiter__` protocol to be compatible with `async for` loops.

### Requirement: Environmental Isolation for Tests
The automated test suite SHALL initialize with a self-contained, valid dummy configuration regardless of the host environment's environment variables.

#### Scenario: Host-Independent Initialization
- **WHEN** a test suite is started in an environment with missing or conflicting GCP variables
- **THEN** it SHALL provide its own default "test" values to allow for safe component initialization without side effects.

### Requirement: Synchronized Instruction Verification
The automated tests for the agent's system instructions SHALL remain synchronized with the actual logic implemented in the agent.

#### Scenario: Verifying Current Instructions
- **WHEN** checking for the presence of rules (e.g., "FORBID the use of any greetings")
- **THEN** the test assertions SHALL match the exact wording used in the implementation to prevent false failures.
