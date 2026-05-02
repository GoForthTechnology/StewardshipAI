## Why

The project requires a specialized research agent that can leverage proprietary documents stored in a GCP Vertex AI RAG Engine. This ensures that the agent's responses are strictly grounded in verified source material, providing high-quality, cited information while minimizing hallucinations.

## What Changes

- Create a dedicated agent implementation that integrates with GCP Vertex AI RAG.
- Configure the agent to connect to the specific RAG corpus: `projects/YOUR_PROJECT_NAME/locations/us-south1/ragCorpora/YOUR_CORPUS_ID`.
- Implement a robust system prompt to enforce groundedness, source lockdown, and citation requirements.
- Provide a clean interface for querying the agent and retrieving responses.

## Capabilities

### New Capabilities
- `gcp-rag-agent`: A research assistant agent that queries a specific GCP Vertex AI RAG corpus to provide grounded answers with citations.

### Modified Capabilities
(None)

## Impact

- Addition of a new agent component.
- Continued dependency on `google-genai` Python library.
- Access requirements for GCP Vertex AI and the specified RAG resources.
