## Context

The current RAG implementation uses Vertex AI's "Managed RAG" tool, where the model automatically handles retrieval and generation in a single step. While efficient, this "black box" approach prevents fine-grained filtering based on file metadata (like extension) unless a formal metadata schema is defined and indexed—a complex infrastructure task. 

This design adopts "Option A": a synthetic RAG pipeline where retrieval and generation are decoupled, allowing the backend to perform manual filtering of results before they are presented to the LLM.

## Goals / Non-Goals

**Goals:**
- Implement a user-controllable extension filter in the UI.
- Transition the agent to a manual Retrieve-Filter-Generate workflow.
- Maintain the "Source Lockdown" mandate by ensuring only filtered official sources are used.

**Non-Goals:**
- Modifying the underlying RAG corpus schema.
- Implementing server-side metadata filtering in Vertex AI ( IaC / Schema work).
- Supporting real-time document type detection (we rely on file extension).

## Decisions

### 1. Decoupled RAG Pipeline
**Decision**: Replace the `types.Tool(retrieval=...)` configuration with explicit calls to `client.models.retrieve`.
**Rationale**: The managed tool does not expose raw chunks for pre-generation filtering. Explicit retrieval gives us access to the `source_uri` of each chunk.

### 2. Extension-to-Mime Mapping
**Decision**: Standardize extension groupings in the backend:
- **PDF**: `.pdf`
- **Word**: `.doc`, `.docx`, `.dotx`
- **TXT**: `.txt`, `.md`, `.csv`, `.json`
- **Other**: Fallback for any other discovered `source_uri` pattern.

### 3. "Synthetic" Grounded Generation
**Decision**: After filtering, the relevant text chunks will be injected into a system prompt using a "Context" block.
**Rationale**: This preserves the grounding benefit of RAG while allowing for the precise inclusion/exclusion of sources.

### 4. UI: Nested Sidebar Controls
**Decision**: Implement extensions as sub-items under each corpus.
**Rationale**: This allows for per-corpus extension filtering (e.g., "PDFs from Magisterium, but Word from Stewardship").

## Risks / Trade-offs

- **[Risk]** Higher Latency → **Mitigation**: The retrieval step is typically fast; the overhead of the second API call to Gemini is acceptable for the increased control.
- **[Risk]** Loss of Automatic Citations → **Mitigation**: We will need to manually format citations in the prompt or response if the user requires them. Since citations were previously "hidden" or simplified, we can maintain the pastoral style by weaving source names into the text manually.
- **[Risk]** Context Window Exhaustion → **Mitigation**: Limit the number of retrieved chunks (e.g., top 10-15) to ensure they always fit within Gemini's 128k+ context window.
