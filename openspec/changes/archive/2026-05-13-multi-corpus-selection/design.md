## Context

The Stewardship AI Portal currently grounds its responses in a fixed set of RAG corpora. The "Source Lockdown" mandate requires all answers to be grounded in these official resources. This design introduces the ability for users to selectively enable or disable specific corpora for a more tailored experience, while maintaining the safety requirement that at least one source is always used.

## Goals / Non-Goals

**Goals:**
- Provide a clear UI in the sidebar for corpus selection.
- Update the communication between frontend and backend to support dynamic corpus lists.
- Refactor the RAG agent to dynamically configure retrieval tools.
- Ensure "Source Lockdown" by preventing empty corpus selections.

**Non-Goals:**
- Allowing users to add *new* RAG corpora through the UI (corpora remain administratively configured).
- Supporting public/web search fallback.

## Decisions

### 1. Corpus Discovery
**Decision**: Update the `/config.js` endpoint to include available corpora.
**Rationale**: This allows the frontend to dynamically render the selection UI based on the backend configuration without hardcoding IDs in the UI.
**Alternatives**: Hardcoding names in the UI (brittle), or a separate `/corpora` endpoint (overkill for this scale).

### 2. API Contract Update
**Decision**: Add `corpus_ids: List[str]` to the `ChatRequest` model.
**Rationale**: Explicit list of IDs is cleaner than boolean flags and supports future expansion to more corpora easily.
**Alternatives**: Boolean flags like `use_magisterium` (not scalable).

### 3. Retrieval Tool Construction
**Decision**: In `rag_agent.py`, iterate through the provided `corpus_ids` and create a unique `types.Tool` for each.
**Rationale**: The Vertex AI GenAI SDK allows multiple tools, each with its own retrieval configuration. This is the idiomatic way to query multiple corpora.
**Alternatives**: A single tool with multiple `rag_resources` (possible, but multiple tools allow for potentially different retrieval settings per corpus in the future).

### 4. Enforcement Logic
**Decision**: Implement "At least one selected" check in the frontend UI (disable the last toggle) and in the backend (raise 400 if empty).
**Rationale**: Provides immediate feedback to the user while maintaining server-side integrity.

## Risks / Trade-offs

- **[Risk]** User disables the most relevant corpus for their query. → **Mitigation**: Clear labels and ensuring the local stewardship corpus is enabled by default.
- **[Risk]** API mismatch between frontend and backend during deployment. → **Mitigation**: Ensure backend supports optional `corpus_ids` defaulting to all available corpora.
