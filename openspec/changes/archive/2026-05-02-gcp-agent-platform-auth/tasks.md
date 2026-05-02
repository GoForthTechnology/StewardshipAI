## 1. Configuration Module

- [x] 1.1 Create `config.py` and implement `GCPConfig` using `pydantic` to manage environment variables.
- [x] 1.2 Add validation to ensure `GCP_PROJECT_ID`, `GCP_LOCATION`, and `GCP_RAG_CORPUS_ID` are present.

## 2. Agent Refactoring

- [x] 2.1 Update `rag_agent.py` to use `GCPConfig` for its initialization.
- [x] 2.2 Refactor `GCPRagAgent` authentication logic to prioritize platform-native ADC while supporting API key fallback.
- [x] 2.3 Remove hardcoded project and location strings from `rag_agent.py`.

## 3. Verification and Cleanup

- [x] 3.1 Update `agent.py` to remove hardcoded corpus paths, relying on environment variables.
- [x] 3.2 Update `verify_rag.py` to test the new environment-driven configuration.
- [x] 3.3 Verify that the agent can be initialized with just environment variables.
