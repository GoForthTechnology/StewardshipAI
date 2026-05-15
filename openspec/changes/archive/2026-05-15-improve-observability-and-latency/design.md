## Context

The Stewardship AI Portal currently lacks granular performance metrics. Users have reported latency, but without tracing, it is difficult to distinguish between time spent in RAG retrieval, document processing, and model generation. Additionally, RAG retrieval currently occurs sequentially for each corpus, which scales poorly as more corpora are added.

## Goals / Non-Goals

**Goals:**
- Provide a clear timing "waterfall" for every chat request in Google Cloud Trace.
- Link application logs to specific traces for faster debugging.
- Reduce latency by parallelizing retrieval tasks.
- Maintain compatibility with Cloud Run's structured logging.

**Non-Goals:**
- Implementing a custom metrics dashboard (rely on GCP native tools).
- Modifying the frontend for client-side tracing.
- Replacing the `google-genai` SDK.

## Decisions

### Decision 1: Centralized Observability Module
- **Rationale**: Create `observability.py` to encapsulate OpenTelemetry initialization. This prevents duplication and ensures that tracing is initialized early in the application lifecycle.
- **Alternatives**: Initializing OTel directly in `api.py` (rejected as it makes `api.py` cluttered and harder to test).

### Decision 2: Native Google Cloud Trace Exporter
- **Rationale**: Use `opentelemetry-exporter-gcp-trace` to send spans directly to Google Cloud. This leverages Application Default Credentials (ADC) and provides a zero-config experience on Cloud Run.
- **Alternatives**: OTLP exporter to a separate collector (rejected as it adds infrastructure complexity).

### Decision 3: Asyncio.gather for Retrieval
- **Rationale**: Since `_manual_retrieve` is an `async` function making network calls, we can use `asyncio.gather` to trigger all retrieval requests concurrently. This reduces the total retrieval time to the duration of the slowest single request.
- **Alternatives**: Sequential loop (Current state - rejected for latency).

### Decision 4: Trace-Aware JSON Logging
- **Rationale**: Extend the `CloudLoggingFormatter` to fetch the current Trace ID from the OpenTelemetry context. By adding `logging.googleapis.com/trace`, Cloud Logging automatically links logs to the corresponding trace.
- **Alternatives**: Logging Trace IDs as plain text (rejected as it doesn't enable the "magic link" in GCP UI).

## Risks / Trade-offs

- **[Risk] Cold Start Overhead** → **Mitigation**: OpenTelemetry initialization adds ~100-200ms to cold starts. We will use the `BatchSpanProcessor` to ensure span export doesn't block request processing.
- **[Risk] Quota Limits** → **Mitigation**: Cloud Trace has generous quotas for standard usage. We will monitor usage and implement sampling if necessary (defaulting to 100% for now).
