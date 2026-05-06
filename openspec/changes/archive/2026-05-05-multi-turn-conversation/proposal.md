## Why

Currently, the chat interface treats every query as an isolated event, forgetting prior context from the same session. This prevents users from asking follow-up questions or having a natural conversational flow about stewardship.

## What Changes

- **API Modification**: Update the `/chat` endpoint to accept a list of previous messages (history) rather than just a single prompt.
- **Frontend Update**: Update the `ChatService` and `PortalComponent` to track and send the full message history to the backend.
- **Agent Enhancement**: Update the `GCPRagAgent` to utilize the provided history in the Gemini content generation process.

## Capabilities

### New Capabilities

### Modified Capabilities
- `api-backend`: Update the chat request schema to support conversation history.
- `web-interface`: Enable sending and displaying multi-turn conversation history.
- `gcp-rag-agent`: Support context-aware response generation using chat history.

## Impact

- `api.py`: `ChatRequest` model and `chat` endpoint logic.
- `rag_agent.py`: `generate_response` and `_get_generate_content_config` methods.
- `frontend/src/app/services/chat.ts`: `streamChat` signature and body.
- `frontend/src/app/components/portal/portal.ts`: `submitChat` logic.
