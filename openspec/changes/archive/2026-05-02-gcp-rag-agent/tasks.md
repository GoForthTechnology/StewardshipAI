## 1. Environment and Setup

- [x] 1.1 Ensure `google-genai` is installed and available in the environment.
- [x] 1.2 Configure GCP credentials and verify access to the target project `YOUR_PROJECT_NAME`.

## 2. Agent Core Implementation

- [x] 2.1 Create `rag_agent.py` and define the `GCPRagAgent` class structure.
- [x] 2.2 Define the strict system instruction as a constant in `rag_agent.py`.
- [x] 2.3 Implement the `__init__` method to initialize the GenAI client with Vertex AI enabled.
- [x] 2.4 Implement a `generate_response` method that configures the `VertexRagStore` and calls the model.
- [x] 2.5 Ensure the response method supports streaming and handles chunk processing.

## 3. Integration and Verification

- [x] 3.1 Refactor `agent.py` to use the new `GCPRagAgent` class or create a new entry point script.
- [x] 3.2 Create a verification script `verify_rag.py` to test the agent against the specific RAG corpus.
- [x] 3.3 Validate that the agent correctly refuses to answer questions outside the corpus scope.
- [x] 3.4 Validate that the agent consistently provides citations in its responses.
