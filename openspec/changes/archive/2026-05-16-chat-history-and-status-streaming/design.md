## Context

The StewardshipAI frontend currently uses a transient `messages` signal to hold chat state. When the page refreshes, the state is lost. On the backend, RAG retrieval and LLM generation are a "black box" until the first byte of text streams back, leading to a perceived lack of progress for the user.

## Goals / Non-Goals

**Goals:**
- Implement persistent chat history using `localStorage`.
- Create a unified SSE protocol for status and text.
- Enable LLM-driven chat titling.
- Maintain the "Source Lockdown" and "Citation" mandates.

**Non-Goals:**
- Server-side history storage (database).
- Multi-device sync.
- Real-time collaboration.

## Decisions

### Decision 1: Local-First Session Model
- **Rationale**: Using `localStorage` allows for immediate persistence without the complexity of a database or backend migration. It fits the current "client-heavy" architecture.
- **Alternatives**: Firestore (rejected for now to keep implementation simple and serverless costs low).

### Decision 2: Status-Text Multiplexing in SSE
- **Rationale**: By sending JSON objects in the `data:` field of the SSE stream, we can easily distinguish between status updates and text chunks. 
- **Format**: `data: {"status": "..."}` or `data: {"text": "..."}`.
- **Alternatives**: Using different SSE event types (e.g., `event: status`). Rejected because JSON parsing the `data` field is more idiomatic for the existing `ChatService` parser.

### Decision 3: Async Title Generation
- **Rationale**: Generating a title is a separate cognitive task for the LLM. Doing it concurrently or after the first message avoids blocking the primary chat response.
- **Alternatives**: Using the first prompt as a title (rejected as prompts can be long and messy).

### Decision 4: Persona-Aware Retrieval Feedback
- **Rationale**: For the `researcher` persona, seeing *which* documents are being analyzed builds trust and provides early value (citations before the answer is even finished).
- **Alternatives**: Always showing document names (rejected for `parishioner` to keep the UI clean and less technical).

## Risks / Trade-offs

- **[Risk] localStorage size limits** → **Mitigation**: We will implement a basic pruning strategy (keeping the last 50 chats) if limits are approached.
- **[Risk] Status-to-Text Transition Jitter** → **Mitigation**: The UI will use a smooth transition (fade-out/fade-in) to replace the status chip with the starting text stream.
- **[Risk] Title Generation Latency** → **Mitigation**: Title generation will be non-blocking and populate the sidebar whenever it completes.
