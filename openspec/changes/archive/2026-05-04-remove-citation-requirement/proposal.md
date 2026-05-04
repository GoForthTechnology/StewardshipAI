## Why

The current requirement for the agent to cite its sources makes it feel less conversational and more like a research tool. Additionally, many of the underlying sources are not publicly available, so providing citations to internal documents can be confusing for users who cannot access the source material.

## What Changes

- **MODIFICATION**: Remove the strict requirement for the agent to provide citations in its responses.
- **MODIFICATION**: Update the system instruction to prioritize a conversational and pastoral tone over structured evidence.
- **MODIFICATION**: Remove citation rendering from the web interface.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `gcp-rag-agent`: Remove citation enforcement and pastoral redirect for missing citations.
- `web-interface`: Remove citation display components and logic.

## Impact

- `rag_agent.py`: System instructions will be updated.
- `api.py`: Streaming response logic for grounding metadata can be simplified or removed.
- `frontend/`: `PortalComponent` and `ChatService` will be updated to remove citation handling.
