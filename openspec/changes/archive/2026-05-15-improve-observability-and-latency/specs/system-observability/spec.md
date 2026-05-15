## ADDED Requirements

### Requirement: Distributed Tracing
The system SHALL implement distributed tracing using OpenTelemetry to track the lifecycle of every chat request from the API entry point through the RAG retrieval and model generation phases.

#### Scenario: Trace Generation
- **WHEN** a chat request is received by the API
- **THEN** the system SHALL start a root trace span.
- **AND** it SHALL create child spans for internal operations including `rag_manual_retrieve`, `context_construction`, and `generation`.

### Requirement: Log Correlation
The system SHALL correlate application logs with distributed traces by injecting the current Trace ID and Span ID into every structured log entry.

#### Scenario: Correlated Log Entry
- **WHEN** a log message is emitted during a traced request
- **THEN** the log entry SHALL include the `logging.googleapis.com/trace` field in the format `projects/[PROJECT_ID]/traces/[TRACE_ID]`.
- **AND** it SHALL include the `logging.googleapis.com/spanId` field.

### Requirement: Infrastructure Instrumention
The system SHALL automatically instrument external dependency calls, specifically HTTP client requests, to capture timing and status data for outgoing service calls.

#### Scenario: Instrumenting Outgoing Requests
- **WHEN** the system makes a REST API call to Vertex AI for retrieval
- **THEN** the OpenTelemetry SDK SHALL automatically capture a child span for that HTTP request.

### Requirement: Performance Metrics Logging
The system SHALL log key performance metrics, such as total request duration and chunk counts, as structured metadata to facilitate dashboarding and alerting.

#### Scenario: Logging Retrieval Metrics
- **WHEN** the retrieval phase completes
- **THEN** the system SHALL set an attribute on the current span with the count of filtered chunks retrieved.
