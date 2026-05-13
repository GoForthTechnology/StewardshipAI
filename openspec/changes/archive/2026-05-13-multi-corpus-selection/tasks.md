## 1. Backend Implementation

- [x] 1.1 Update `ChatRequest` in `api.py` to include `corpus_ids: Optional[List[str]] = None`.
- [x] 1.2 Update `get_frontend_config` in `api.py` to include available corpora in the `window.ENV` response.
- [x] 1.3 Update `stream_agent_response` in `api.py` to accept and pass `corpus_ids`.
- [x] 1.4 Update `GCPRagAgent._get_generate_content_config` in `rag_agent.py` to dynamically construct retrieval tools based on `corpus_ids`.
- [x] 1.5 Update `GCPRagAgent.generate_response` in `rag_agent.py` signature and internal calls to pass `corpus_ids`.

## 2. Frontend Service & State

- [x] 2.1 Update `ChatService.streamChat` in `frontend/src/app/services/chat.ts` to accept and send `corpus_ids`.
- [x] 2.2 Define `Corpus` interface and update state in `frontend/src/app/components/portal/portal.ts`.
- [x] 2.3 Initialize available corpora from `window.ENV` in the `PortalComponent`.

## 3. Frontend UI Component

- [x] 3.1 Add corpus selection section to the sidebar template in `portal.ts`.
- [x] 3.2 Implement `toggleCorpus` logic in `portal.ts` with "at least one" enforcement.
- [x] 3.3 Ensure the Magisterium corpus is disabled by default in the initial state.
- [x] 3.4 Pass selected corpus IDs to `chatService.streamChat` in `submitChat`.
- [x] 3.5 Style the toggles to match the existing brand aesthetics.

## 4. Verification

- [x] 4.1 Verify that disabling a corpus correctly excludes it from the agent's context.
- [x] 4.2 Verify that at least one corpus must be selected (UI and API).
- [x] 4.3 Run `verify_rag.py` to ensure no regressions in RAG grounding.
