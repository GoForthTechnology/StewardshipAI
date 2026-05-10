## Why

The Stewardship AI Portal needs to support users who wish to revise academic or complex texts (such as theses, reports, or articles) into approachable, pastoral language. Currently, the RAG agent only uses pre-indexed corpora and lacks the full context of a user's specific document, making it difficult to synthesize complex concepts with modern analogies found in recent sources.

## What Changes

- **Document Upload Capability**: Users can upload a PDF or text document (up to 10MB) that persists as a session-local context.
- **Hybrid Context Logic**: The RAG agent will use both the uploaded document (as the primary subject) and the existing RAG corpora (as the reference for analogies and tone) to generate responses.
- **UI Enhancements**: Added an upload button, file selection safeguards, and a "File Chip" to indicate the active context in the chat interface.
- **Refined Researcher Persona**: Update the `RESEARCHER_INSTRUCTION` to prioritize academic-to-approachable translation and analogy mining.

## Capabilities

### New Capabilities
- `session-file-context`: Requirements for uploading, storing, and referencing session-persistent files within the GenAI context window.
- `document-translator-logic`: Requirements for the "Hybrid" synthesis behavior, prioritizing the uploaded document as the primary source for revision.

### Modified Capabilities
- `web-interface`: Add support for file upload UI components, size/type validation, and persistent file status display.
- `gcp-rag-agent`: Update the agent to handle multiple context sources (extracted text from local files + RAG retrieval) simultaneously.

## Impact

- **Frontend**: `portal.ts`, `chat.ts`, and new CSS for file chips.
- **Backend**: `api.py` (new `/upload` endpoint with local storage), `rag_agent.py` (updated logic with text extraction via `pypdf`).
- **Dependencies**: Added `pypdf` to `requirements.txt`.
