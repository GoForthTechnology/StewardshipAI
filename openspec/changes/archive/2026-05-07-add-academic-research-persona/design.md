## Context

The StewardshipAI platform uses a persona-based approach to tailor RAG agent responses. Currently, it supports "Priest" and "Parishioner". The logic is distributed across `rag_agent.py` (system instructions), `api.py` (request handling), and several Angular components.

## Goals / Non-Goals

**Goals:**
- Implement a first-class "Academic / Researcher" persona.
- Provide high-quality synthesis and citation behavior for the research persona.
- Expose the new persona in the web UI.

**Non-Goals:**
- Creating a separate RAG corpus for academics (we use the existing one).
- Persistent user-defined personas (sticking to the three predefined roles).

## Decisions

### 1. Instruction Definition
**Decision**: Add `RESEARCHER_INSTRUCTION` to `rag_agent.py`.
**Rationale**: Keeps all persona-specific logic in one place.
**Alternatives**: Moving instructions to a database. (Rejected: Overkill for three static personas).

### 2. Frontend Persona Typing
**Decision**: Update the `Persona` union type in `stewardship.ts`.
**Rationale**: Provides type safety throughout the Angular application.

### 3. Component Updates
**Decision**: Manually update `portal.ts` and `discovery-grid.ts` templates.
**Rationale**: Simple and follows the existing pattern for the other two personas.

## Risks / Trade-offs

- **[Risk] Prompt Injection / Persona Confusion** → **Mitigation**: Ensure `_get_generate_content_config` strictly maps the input string to the valid instruction set.
- **[Risk] Citation Hallucination** → **Mitigation**: The `RESEARCHER_INSTRUCTION` will explicitly command the model to only cite sources present in the retrieved context.
