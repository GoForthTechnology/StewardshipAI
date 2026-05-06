## Context

The application's backend is built with FastAPI, which uses an asynchronous event loop. However, the current implementation of the chat streaming logic uses synchronous loops and synchronous SDK clients. This blocks the event loop, causing the application to become unresponsive (hang) when a request is slow or when multiple requests occur. Additionally, there are no timeouts in the frontend or backend to recover from stalled states.

## Goals / Non-Goals

**Goals:**
- Eliminate event loop blocking by migrating to fully asynchronous I/O for chat generation.
- Implement a 60-second server-side timeout for agent generation.
- Implement a 15-second client-side timeout for the initial connection.
- Ensure the backend remains responsive to health checks and other requests during long-running chat sessions.

**Non-Goals:**
- Completely rewriting the RAG logic or switching to a different LLM provider.
- Implementing persistent session storage (timeouts remain ephemeral).

## Decisions

### 1. Asynchronous Google GenAI Client
Migrate from `client.models` to `client.aio.models`.
- **Rationale**: The `aio` client is specifically designed for `async/await` patterns in Python, allowing the event loop to yield while waiting for streaming chunks from Vertex AI.
- **Alternatives**: Using `run_in_executor` to offload synchronous calls to a thread pool (adds complexity and overhead).

### 2. `asyncio.timeout` for Backend
Wrap the generation loop in an `asyncio.timeout` block.
- **Rationale**: Provides a native, lightweight way to ensure an async block does not exceed a time limit.

### 3. `AbortController` for Frontend
Use the standard Web `AbortController` API in the Angular service.
- **Rationale**: Allows the frontend to programmatically cancel a `fetch` request if it takes too long or if the user navigates away.

## Risks / Trade-offs

- **[Risk]** Improper async cleanup leading to leaked connections. → **Mitigation**: Use `async with genai.Client(...)` or ensure the shared client's lifecycle is managed correctly.
- **[Risk]** Complex error states in the UI. → **Mitigation**: Standardize error messages so the user knows if it was a timeout or a real failure.
