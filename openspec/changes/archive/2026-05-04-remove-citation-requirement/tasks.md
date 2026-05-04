## 1. Backend Refactor (Python)

- [x] 1.1 Update `SYSTEM_INSTRUCTION` in `rag_agent.py` to remove citation rules and emphasize conversational tone.
- [x] 1.2 Modify `stream_agent_response` in `api.py` to skip yielding `citations` chunks from grounding metadata.

## 2. Frontend Cleanup (Angular)

- [x] 2.1 Update `ChatMessage` interface in `frontend/src/app/services/chat.ts` to remove the optional `citations` field.
- [x] 2.2 Remove citation deduplication and assignment logic from `submitChat` in `frontend/src/app/components/portal/portal.ts`.
- [x] 2.3 Remove the citations rendering template block from `portal.ts`.

## 3. Verification

- [x] 3.1 Run `verify_rag.py` to ensure the agent still provides grounded answers without explicit citations.
- [x] 3.2 Manually verify the chat interface in the browser to confirm no citation links appear.
