## Why

Users who author their own documents (often in Word format) want the ability to restrict the RAG grounding process to specific document types. This allows them to focus the agent's "knowledge" on their own authored work or specific data formats (PDF, TXT, etc.) without the overhead of re-indexing or re-organizing the underlying RAG corpora.

## What Changes

- **Extension Multi-Select UI**: Add nested checkboxes under each RAG corpus in the sidebar to allow users to select which file extensions (PDF, Word, TXT, Other) to include in the query.
- **Enhanced API Contract**: Update the `/chat` endpoint to accept a map or list of allowed extensions per request.
- **Manual RAG Pipeline (Option A)**: Transition the backend from "Managed RAG" (one-step tool call) to a "Synthetic RAG" flow:
  1.  **Retrieve**: Explicitly fetch relevant chunks from Vertex AI.
  2.  **Filter**: Use Python to filter these chunks by checking the `source_uri` file extension.
  3.  **Generate**: Pass the filtered context to Gemini for final response generation.
- **Extension Logic**: Standardize extension groupings (e.g., Word includes `.doc` and `.docx`).

## Capabilities

### New Capabilities
- `extension-filtering-ui`: Provides nested multi-select controls for file extensions within the corpus selection UI.
- `synthetic-rag-filtering`: Implements the manual retrieval, Python-based extension filtering, and grounded generation pipeline.

### Modified Capabilities
- `gcp-rag-agent`: Update the agent implementation to move away from the managed tool-call abstraction in favor of the manual retrieve-then-generate workflow.

## Impact

- `api.py`: Updated `ChatRequest` model and `/chat` handler logic.
- `rag_agent.py`: Significant refactor of `generate_response` and helper methods to support manual retrieval and filtering.
- `frontend/src/app/components/portal/portal.ts`: Updated sidebar template and state management for nested extension toggles.
- `frontend/src/app/services/chat.ts`: Service updated to pass extension filters to the backend.
- `frontend/src/app/services/stewardship.ts`: May need updates to handle extension preference persistence.
