## Context

The StewardshipAI portal provides a chat interface for users to learn about Time, Talent, and Treasure. Currently, the `api.py` and `rag_agent.py` expect a single `prompt` string. The frontend maintains an array of `ChatMessage` objects for display but only sends the latest input string to the server.

## Goals / Non-Goals

**Goals:**
- Maintain conversation context across multiple turns in a single session.
- Support follow-up questions (e.g., "Tell me more about that").
- Keep the implementation simple by passing history from the client to the server (stateless backend).

**Non-Goals:**
- Long-term persistent storage of chat history in a database (history is ephemeral/session-based).
- Multi-user "shared" conversations.

## Decisions

### 1. Data Contract: `ChatMessage` List
The `/chat` endpoint will now accept a `history` field in the request body.
- **Decision**: `ChatRequest` will include `history: List[Message]` where `Message` has `role` and `content`.
- **Rationale**: This is the standard pattern for LLM APIs and avoids needing complex session management on the backend.

### 2. Backend Processing: Gemini Content Structure
The `GCPRagAgent` will be updated to accept the history and convert it into the `types.Content` format required by the Google GenAI SDK.
- **Decision**: The history will be prepended to the user's latest prompt.
- **Rationale**: Ensures the RAG retrieval and the final generation have context of what was already discussed.

### 3. Frontend: Cumulative History
The `PortalComponent` already tracks messages in a signal.
- **Decision**: Pass the current value of the `messages` signal (excluding the final assistant placeholder) to the `ChatService`.
- **Rationale**: Minimizes code changes while achieving full context.

## Risks / Trade-offs

- **[Risk]** Context Window Overflow: Sending every message back could eventually hit token limits. → **Mitigation**: For this prototype, we will send the full history. A future refinement could implement a "sliding window" (e.g., last 10 messages).
- **[Risk]** Latency: Larger payloads increase request size. → **Mitigation**: Text data is small; impact will be negligible for typical stewardship conversations.
