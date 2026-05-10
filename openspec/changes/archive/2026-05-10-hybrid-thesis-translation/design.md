## Context

The StewardshipAI application currently relies entirely on pre-indexed RAG corpora. Authors revising long-form academic or complex texts struggle because they must copy-paste snippets into the chat, losing the broader structural context of their work. We need a way to ingest a document as a primary "Anchor" context while using the RAG corpora as a "Reference" for modernizing the language.

## Goals / Non-Goals

**Goals:**
- Implement a session-persistent document upload mechanism.
- Integrate the document content into the Gemini context window alongside RAG tools.
- Enforce strict safeguards (10MB limit, PDF/Text only).
- Provide visual feedback in the UI for the active document context.
- Update the "Researcher" persona to support academic-to-approachable translation for any complex text.

**Non-Goals:**
- Permanent storage of uploaded files in a database (Files are ephemeral).
- Multi-file uploads (Scope limited to one primary document per session for now).

## Decisions

### Decision 1: Local File Storage and Text Extraction
- **Rationale**: The Google GenAI SDK's `files` service is exclusive to Google AI Studio and not supported on Vertex AI. Additionally, Vertex AI grounding/RAG currently restricts multimodal inputs (like raw PDF bytes) when grounding tools are active.
- **Solution**: Uploaded files are stored in a temporary local directory (`/tmp/stewardship-uploads`). The backend uses `pypdf` to extract text from PDFs.
- **Alternative**: GCS Storage (Rejected: Adding unnecessary latency for temporary session context).

### Decision 2: Context Injection via Text Parts
- **Rationale**: To bypass the "grounding not supported for non-text input" 400 error, we inject the extracted text as a standard string part in the `contents` list. This satisfies the "text-only" requirement for grounding while providing the full document context.
- **Alternatives**: Two-step inference (Rejected: Double the cost and latency).

### Decision 3: Backend-Controlled File Safeguards
- **Rationale**: Validation (size and type) occurs both on the frontend (for UX) and backend (for security). A 10MB limit is enforced.

### Decision 4: Frontend "Document Chip" Persistence
- **Rationale**: The `file_uri` (local path) returned by `/upload` is stored in the Angular component state and included in chat requests until removed.

## Risks / Trade-offs

- **[Risk] Extraction Quality** → **Mitigation**: Using `pypdf`, which is standard for text-heavy academic documents. We provide fallback to plain text for non-PDF files.
- **[Trade-off] Multi-user Isolation** → **Rationale**: Current implementation uses `/tmp` with random UUIDs. While sufficient for private LAN use, future multi-tenant deployments should use user-scoped subdirectories.
