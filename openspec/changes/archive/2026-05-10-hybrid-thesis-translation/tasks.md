## 1. Backend: File Upload & Storage

- [x] 1.1 Implement `POST /upload` endpoint in `api.py` with size (10MB) and type (PDF/Text) validation.
- [x] 1.2 Integrate Google GenAI `files` API to handle ephemeral storage and return `file_uri`.
- [x] 1.3 Add error handling for failed uploads and invalid file formats.

## 2. Backend: Hybrid RAG Agent

- [x] 2.1 Update `GCPRagAgent.generate_response` in `rag_agent.py` to accept an optional `file_uri`.
- [x] 2.2 Modify `generate_content` payload to prepend file parts to the message context if `file_uri` is present.
- [x] 2.3 Update `RESEARCHER_INSTRUCTION` in `rag_agent.py` to prioritize academic-to-approachable synthesis and analogy mining.

## 3. Frontend: Upload UI

- [x] 3.1 Add a hidden `<input type="file">`, a "📎" button, and a small hint text ("PDF/TXT only") to the chat input form in `portal.ts`.
- [x] 3.2 Implement `onFileSelected` logic with frontend validation for size and type.
- [x] 3.3 Create a "File Chip" UI component above the chat input to display the uploaded file name with a "remove" button.

## 4. Frontend: API Integration

- [x] 4.1 Update `ChatService` in `chat.ts` to support file uploading and passing `file_uri` in the chat request.
- [x] 4.2 Update `PortalComponent` to manage the active file state across chat turns.
- [x] 4.3 Ensure "Reset Chat" clears the active file context.

## 5. Verification

- [x] 5.1 Verify 10MB file size limit enforcement.
- [x] 5.2 Verify that the agent correctly references the uploaded thesis and recent RAG sources in a single response.
- [x] 5.3 Run `verify_rag.py` to ensure no regressions in existing persona behaviors.
