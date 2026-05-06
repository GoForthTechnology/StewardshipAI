## 1. Backend API Updates

- [x] 1.1 Update `ChatRequest` model in `api.py` to include `history: Optional[List[dict]] = None`.
- [x] 1.2 Update `/chat` endpoint in `api.py` to pass history to `stream_agent_response`.
- [x] 1.3 Update `stream_agent_response` generator to pass history to `agent.generate_response`.

## 2. RAG Agent Updates

- [x] 2.1 Update `GCPRagAgent.generate_response` in `rag_agent.py` to accept `history`.
- [x] 2.2 Update `GCPRagAgent._get_generate_content_config` to handle history (future-proofing).
- [x] 2.3 Implement history-to-content conversion in `generate_response` using the Google GenAI SDK's `types.Content` structure.

## 3. Frontend Service Updates

- [x] 3.1 Update `ChatService.streamChat` in `frontend/src/app/services/chat.ts` to accept `history: ChatMessage[]`.
- [x] 3.2 Update the `fetch` body in `streamChat` to include the `history`.

## 4. Frontend Component Updates

- [x] 4.1 Update `PortalComponent.submitChat` in `frontend/src/app/components/portal/portal.ts` to pass the current messages as history.
- [x] 4.2 Ensure the placeholder message (the one currently being filled) is not included in the history sent to the server.

## 5. Verification

- [x] 5.1 Verify that the first question works as expected.
- [x] 5.2 Verify that a follow-up question (e.g., "Tell me more about the first point") correctly references prior context.
- [x] 5.3 Verify that the animated bubble still works correctly with multi-turn history.
