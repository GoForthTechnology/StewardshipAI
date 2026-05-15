## Why

Users have reported high latency in chat responses. To diagnose and address this, we need better visibility into the application's internal request-response lifecycle and optimizations to the RAG retrieval process.

## What Changes

- **OpenTelemetry Tracing**: Implement distributed tracing using OpenTelemetry to track requests across the backend and external service calls (Vertex AI).
- **Log Correlation**: Align backend logs with Cloud Trace IDs to enable side-by-side analysis of timing and logs in the Google Cloud Console.
- **Parallel RAG Retrieval**: Optimize the RAG agent to fetch chunks from multiple corpora in parallel instead of sequentially, reducing the "Retrieval Phase" duration.
- **Backend Instrumentation**: Add manual spans for critical operations (RAG search, LLM generation) to provide granular performance metrics.

## Capabilities

### New Capabilities
- `system-observability`: Requirements for distributed tracing, log correlation, and performance monitoring.

### Modified Capabilities
- `gcp-rag-agent`: Update retrieval logic to support concurrent execution across multiple resource corpora.

## Impact

- **Backend**: `api.py`, `rag_agent.py`, and a new `observability.py` module.
- **Infrastructure**: Requires `Cloud Trace Agent` IAM permissions for the service account.
- **Dependencies**: New OpenTelemetry and Google Cloud Trace SDKs in `requirements.txt`.
