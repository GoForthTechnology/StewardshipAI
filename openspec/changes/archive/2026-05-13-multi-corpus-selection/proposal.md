## Why

Currently, the Stewardship AI Portal always performs retrieval from all configured RAG corpora (e.g., local stewardship resources and the universal Magisterium corpus). Users want the ability to explicitly control which corpora are used for grounding their queries to focus on either practical local guidance or universal doctrine, or both.

## What Changes

- **UI Corpus Controls**: Add toggle switches in the portal sidebar to enable or disable individual corpora.
- **Selection Enforcement**: Implement logic to ensure at least one corpus is selected at all times, adhering to the "Source Lockdown" mandate which forbids using only public/general knowledge.
- **Default Selection**: The local Stewardship corpus SHALL be enabled by default, while the Universal Magisterium corpus SHALL be disabled by default.
- **Backend API Update**: Modify the `/chat` endpoint to accept an optional list of active corpus IDs.
- **Dynamic Retrieval**: Update the RAG agent to construct its retrieval tools based on the user's specific selection for each request.

## Capabilities

### New Capabilities
- `corpus-selection-ui`: Provides UI components for users to view and toggle available RAG corpora.

### Modified Capabilities
- `magisterium-retrieval`: Update requirements to allow for *optional* inclusion of the Magisterium corpus based on user preference, rather than mandatory dual retrieval.
- `gcp-rag-agent`: Update the agent implementation to handle dynamic corpus lists provided per-request.

## Impact

- `api.py`: Updated `ChatRequest` model and request handling logic.
- `rag_agent.py`: Updated configuration generation to support a variable number of retrieval tools.
- `frontend/src/app/components/portal/portal.ts`: New UI state for active corpora and updated submission logic.
- `frontend/src/app/services/chat.ts`: Service updated to pass corpus selection to the backend.
- `config.py`: May need updates to expose corpus display names if not already present.
