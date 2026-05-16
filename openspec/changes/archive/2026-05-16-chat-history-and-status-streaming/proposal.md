## Why

The current StewardshipAI interface is a single-turn query engine that feels disconnected from modern LLM expectations. Users familiar with ChatGPT expect conversation persistence, immediate feedback on background tasks, and a sense of "thinking" through status updates, especially during long RAG retrieval phases.

## What Changes

- **Chat History Persistence**: Switch from ephemeral sessions to a local-first persistent history using `localStorage`, allowing users to resume past conversations.
- **Status Streaming**: Introduce a real-time status protocol to the SSE stream, informing the user about specific backend actions (searching, reading, synthesizing).
- **Dynamic Title Generation**: Automatically generate concise titles for new chats using the LLM.
- **Persona-Aware Citations**: Enhance the "Researcher" persona to include specific document references in the status stream.

## Capabilities

### New Capabilities
- `chat-persistence`: Requirements for managing local-first chat sessions and history navigation.
- `status-streaming-protocol`: Requirements for the end-to-end communication of agent internal states to the UI.

### Modified Capabilities
- `web-interface`: Update UI to support a history sidebar and animated status indicators.
- `gcp-rag-agent`: Update agent to support status yielding and dynamic title generation.

## Impact

- **Frontend**: `portal.ts`, `chat.ts`, and a new `history.ts` service.
- **Backend**: `api.py` (new title endpoint, updated stream) and `rag_agent.py` (async generator for status).
- **Data**: Client-side `localStorage` schema for chat sessions.
