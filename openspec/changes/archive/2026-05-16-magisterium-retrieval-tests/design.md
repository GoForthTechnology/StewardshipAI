## Context

The `GCPRagAgent` currently retrieves chunks from multiple corpora in parallel but does not distinguish between them when constructing the prompt context. Chunks are simply concatenated under `OFFICIAL SOURCE CONTEXT`. This makes it difficult for the model to follow the "Source Hierarchy" (Universal Doctrine > Practical Application) defined in the system instructions.

## Goals / Non-Goals

**Goals:**
- Implement "Chunk Labeling" in the context construction to identify the source corpus for each piece of text.
- Update `SYSTEM_INSTRUCTION` to reference these labels for prioritization.
- Add comprehensive unit tests in `test_retrieval_hierarchy.py` to verify the "Traceability Firewall" for Magisterium retrieval.

**Non-Goals:**
- Implementing a separate "Intent Detection" classifier (we will rely on the LLM's adherence to the hierarchy instructions).
- Modifying the frontend corpus selection UI.

## Decisions

### 1. Context Labeling
**Decision**: When constructing the `synthetic_context`, each chunk will be prefixed with its Source Category (e.g., `[SOURCE: Magisterium Corpus]`).
**Rationale**: This provides clear metadata to the LLM to apply the hierarchy rules without requiring a complex multi-stage prompt.
**Alternatives**: 
- Separate prompt parts: More expensive and complex to manage with history.
- Multi-stage reasoning (CoT): Higher latency.

### 2. Test Isolation
**Decision**: Create `test_retrieval_hierarchy.py` using `unittest.IsolatedAsyncioTestCase` and `test_utils._AsyncIterator`.
**Rationale**: Keeps the Magisterium-specific logic tests decoupled from general agent plumbing tests.

## Risks / Trade-offs

- [Risk] → Model ignores labels and synthesizes incorrectly.
- [Mitigation] → Use "Golden Response" test cases in `test_retrieval_hierarchy.py` that check for specific doctrinal keyphrases when conflicting info is provided.
