## Why

The application currently experiences hangs and unresponsiveness during chat interactions. This is caused by synchronous, blocking I/O calls within the FastAPI asynchronous event loop, which prevents the server from processing concurrent requests or managing connection lifecycle events.

## What Changes

- **Asynchronous Backend**: Convert the RAG agent and API streaming logic to use the fully asynchronous `aio` client from the Google GenAI SDK.
- **Backend Resilience**: Implement an asynchronous timeout mechanism for generation requests to prevent indefinite hangs.
- **Frontend Resilience**: Implement a request timeout and abort logic in the frontend to handle unresponsive server states gracefully.
- **Enhanced Error Handling**: Provide specific user feedback for timeout events versus general network failures.

## Capabilities

### New Capabilities

### Modified Capabilities
- `api-backend`: Implement asynchronous request processing and backend timeouts.
- `gcp-rag-agent`: Migrate to asynchronous content generation.
- `web-interface`: Add request timeout and specific error handling for hangs.

## Impact

- `api.py`: `stream_agent_response` and `/chat` endpoint.
- `rag_agent.py`: `generate_response` and `_get_generate_content_config`.
- `frontend/src/app/services/chat.ts`: `streamChat` fetch logic.
- `frontend/src/app/components/portal/portal.ts`: `submitChat` error handling.
