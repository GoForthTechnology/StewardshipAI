## 1. Backend: Synthetic RAG Logic

- [x] 1.1 Update `ChatRequest` in `api.py` to accept `extension_filters: Dict[str, List[str]]`.
- [x] 1.2 Implement extension grouping logic in `rag_agent.py` (mapping Word -> docx, etc.).
- [x] 1.3 Refactor `GCPRagAgent` to split retrieval and generation steps.
- [x] 1.4 Implement filtering logic in `GCPRagAgent` based on `source_uri`.
- [x] 1.5 Update `generate_response` to inject filtered chunks into the system prompt.

## 2. Frontend: Nested UI Controls

- [x] 2.1 Update `Corpus` interface in `portal.ts` to include `extensionFilters`.
- [x] 2.2 Add nested checkbox template for extension filtering in the sidebar.
- [x] 2.3 Implement toggle logic for individual extensions.
- [x] 2.4 Update `ChatService.streamChat` to pass extension filters to the backend.

## 3. Verification

- [x] 3.1 Verify that selecting only "Word" correctly filters out PDF-based RAG results.
- [x] 3.2 Verify that selecting multiple extensions works correctly.
- [x] 3.3 Verify "Source Lockdown" is maintained (model doesn't use outside knowledge if filters exclude all RAG results).
- [x] 3.4 Regression test session file uploads alongside filtered RAG results.
