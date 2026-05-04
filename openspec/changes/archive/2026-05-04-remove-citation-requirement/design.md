## Context

The current StewardshipAI agent is configured to be a strict research assistant that must provide citations for every claim. This was appropriate for the initial research-focused prototype but is now hindering the desired pastoral and conversational tone for the Diocese. The system uses Vertex AI Search (RAG) and the `google-genai` Python SDK on the backend, with an Angular frontend.

## Goals / Non-Goals

**Goals:**
- Refactor the `SYSTEM_INSTRUCTION` in `rag_agent.py` to remove the citation requirement.
- Simplify the response processing in `api.py` and the Angular frontend.
- Maintain the grounding in official diocesan documents without displaying the source metadata to the user.

**Non-Goals:**
- Removing the RAG capability itself; the agent should still only use the provided corpus.
- Changing the authentication or API structure.

## Decisions

- **Simplified System Instruction**: We will remove the "Citations" and "Citation Enforcement" rules from the `SYSTEM_INSTRUCTION`. We will replace them with instructions to weave information naturally into a warm, pastoral conversation.
- **Backend Data Pruning**: The `api.py` currently yields `citations` chunks extracted from `grounding_metadata`. We will modify the generator to skip these chunks, reducing payload size and complexity.
- **Frontend Cleanup**: The `PortalComponent` in Angular will be updated to remove the citations template and the deduplication logic in `submitChat`.

## Risks / Trade-offs

- **[Risk] Reduced Transparency** → **Mitigation**: The agent will still be strictly grounded. We will monitor responses for hallucinations during verification.
- **[Trade-off] Loss of "Strict Research" functionality** → **Rationale**: The user has explicitly requested a more conversational "Guide" persona over a "Research" persona.
