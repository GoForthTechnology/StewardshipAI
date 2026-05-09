## 1. Backend Implementation

- [x] 1.1 Add `RESEARCHER_INSTRUCTION` to `rag_agent.py` with focus on synthesis and citations
- [x] 1.2 Update `_get_generate_content_config` in `rag_agent.py` to map the `researcher` persona string to the new instruction set and label

## 2. Frontend Infrastructure

- [x] 2.1 Update the `Persona` type definition in `frontend/src/app/services/stewardship.ts` to include `'researcher'`

## 3. UI Components

- [x] 3.1 Update `frontend/src/app/components/portal/portal.ts` to include a navigation button for the "Academic / Researcher" persona
- [x] 3.2 Update `frontend/src/app/components/discovery-grid/discovery-grid.ts` to show research-specific discovery prompts when the researcher persona is active

## 4. Verification

- [ ] 4.1 Manually verify that switching to the Researcher persona updates the discovery grid
- [ ] 4.2 Submit a research query and verify the agent provides a synthesized response with citations
- [ ] 4.3 Run `verify_rag.py` to ensure core RAG functionality remains stable
