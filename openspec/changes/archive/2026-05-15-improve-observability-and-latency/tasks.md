## 1. Dependency Management

- [x] 1.1 Add OpenTelemetry and GCP Trace packages to `requirements.txt`
- [x] 1.2 Verify package availability and compatibility

## 2. Infrastructure & Core Module

- [x] 2.1 Create `observability.py` module for OTel initialization
- [x] 2.2 Implement `setup_observability` helper with `CloudTraceSpanExporter`
- [x] 2.3 Implement Trace and Span ID retrieval utilities for log correlation

## 3. API Integration

- [x] 3.1 Import and initialize observability in `api.py`
- [x] 3.2 Update `CloudLoggingFormatter` in `api.py` to inject `logging.googleapis.com/trace` fields
- [x] 3.3 Instrument FastAPI app with `FastAPIInstrumentor`
- [x] 3.4 Ensure global `httpx` clients are instrumented

## 4. Agent Optimization & Instrumentation

- [x] 4.1 Update `rag_agent.py` to import and use the OpenTelemetry tracer
- [x] 4.2 Instrument `_manual_retrieve` with spans and metadata attributes
- [x] 4.3 Refactor `generate_response` to parallelize multi-corpus retrieval using `asyncio.gather`
- [x] 4.4 Add manual spans for context construction and generation phases in `rag_agent.py`

## 5. Verification

- [x] 5.1 Run `api.py` locally and verify JSON logs contain trace fields
- [x] 5.2 Verify that parallel retrieval correctly aggregates results from all corpora
- [x] 5.3 (Integration) Deploy to Cloud Run and verify trace appearance in GCP Console
