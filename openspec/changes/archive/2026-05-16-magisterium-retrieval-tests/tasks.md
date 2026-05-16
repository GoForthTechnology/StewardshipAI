## 1. Preparation

- [x] 1.1 Create `test_retrieval_hierarchy.py` following the async mocking pattern in `test_rag_agent.py`

## 2. Implementation: Context Labeling & Synthesis

- [x] 2.1 Update `GCPRagAgent.generate_response` to track which chunks come from which corpus ID
- [x] 2.2 Implement chunk labeling in `synthetic_context` (e.g., `[SOURCE: <corpus_id>] <text>`)
- [x] 2.3 Update `SYSTEM_INSTRUCTION` in `rag_agent.py` to instruct the model to prioritize `[SOURCE: <magisterium_id>]` for theological questions

## 3. Implementation: Test Scenarios

- [x] 3.1 Implement `test_Scenario_Querying_with_Selected_Corpora` asserting correct `corpus_id` in REST calls
- [x] 3.2 Implement `test_Scenario_Synthesis_of_Universal_Doctrine` using competing mocks to verify doctrinal priority
- [x] 3.3 Implement `test_Scenario_Local_Application_of_Doctrine` using competing mocks to verify practical grounding

## 4. Verification

- [x] 4.1 Run `pytest test_retrieval_hierarchy.py`
- [x] 4.2 Run `verify_coverage.py` to confirm 100% status for `magisterium-retrieval`
