## Why

The StewardshipAI application currently supports two personas: "Priest" and "Parishioner". However, with the recent addition of a larger corpus of stewardship documents and academic research papers, there is a need to support users engaged in deep study, synthesis, and academic writing. This change introduces an "Academic / Researcher" persona to empower priests and academics to leverage the RAG corpus for research purposes.

## What Changes

- **New Persona**: Introduction of the "Academic / Researcher" persona across the entire stack.
- **RAG Agent Instructions**: Addition of specific system instructions for the research persona, focusing on synthesis, cross-document analysis, and rigorous citations.
- **Frontend Navigation**: A new selection option for the Academic persona in the portal sidebar.
- **Discovery Grid**: Tailored suggested prompts for academic research and theological synthesis.
- **Persona Persistence**: The frontend service will support the new persona type.

## Capabilities

### New Capabilities
- `academic-research-persona`: Requirements for the new Academic / Researcher persona, including its unique instruction set and expected output behavior (e.g., synthesis and citations).

### Modified Capabilities
- `gcp-rag-agent`: Modification of the role-based response tailoring to include the new Academic persona.
- `web-interface`: Update to the navigation and discovery components to expose the new persona.

## Impact

- `rag_agent.py`: New system instruction constant and logic to select it.
- `frontend/src/app/services/stewardship.ts`: Update to `Persona` type.
- `frontend/src/app/components/portal/portal.ts`: Sidebar UI update.
- `frontend/src/app/components/discovery-grid/discovery-grid.ts`: Discovery grid UI update.
