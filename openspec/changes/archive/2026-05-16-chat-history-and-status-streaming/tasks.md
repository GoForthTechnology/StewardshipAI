## 1. Backend Status Streaming & Titling

- [x] 1.1 Refactor `GCPRagAgent.generate_response` in `rag_agent.py` to yield status dictionaries before text chunks.
- [x] 1.2 Implement persona-aware document identification logic for the "Researcher" persona status updates.
- [x] 1.3 Update `stream_agent_response` in `api.py` to handle the new generator and emit multiplexed JSON SSE events.
- [x] 1.4 Create the `/chat/title` POST endpoint in `api.py` for LLM-driven chat summarization.

## 2. Frontend Services & Persistence

- [x] 2.1 Create `HistoryService` in `frontend/src/app/services/history.ts` to manage `localStorage` operations.
- [x] 2.2 Update `ChatService.streamChat` in `chat.ts` to parse multiplexed JSON (status vs text) from the SSE stream.
- [x] 2.3 Implement the `/chat/title` caller in `ChatService`.

## 3. UI Implementation

- [x] 3.1 Refactor `PortalComponent` sidebar to display "Recent Chats" list from `HistoryService`.
- [x] 3.2 Add `currentStatus` signal to `PortalComponent` and update the template to show the status chip.
- [x] 3.3 Implement chat session switching logic (loading history into the active view).
- [x] 3.4 Implement auto-titling trigger after the first turn of a new chat.

## 4. Verification

- [x] 4.1 Verify status streaming "Thinking" phase in UI.
- [x] 4.2 Verify history persistence across page refreshes.
- [x] 4.3 Verify LLM title generation for new chats.
