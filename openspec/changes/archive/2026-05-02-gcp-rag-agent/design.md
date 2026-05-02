## Context

The current project contains a basic script (`agent.py`) demonstrating a connection to Vertex AI RAG. To build a robust application, we need a formalized, reusable agent component that enforces strict grounding and citation requirements. This change will move from a script-based approach to a more modular agent design.

## Goals / Non-Goals

**Goals:**
- Implement a reusable `GCPRagAgent` class that encapsulates interaction with Vertex AI RAG Engine.
- Enforce strict system instructions to ensure the agent only uses provided sources and provides citations.
- Provide a clean, asynchronous interface for querying the agent.
- Ensure the agent handles cases where information is missing by gracefully refusing to answer.

**Non-Goals:**
- Building a user interface (CLI or Web).
- Implementing RAG corpus management (uploading, indexing).
- Supporting multiple RAG corpora simultaneously (out of scope for initial implementation).

## Decisions

- **Framework**: Use the `google-genai` Python library for its modern, clean interface to Vertex AI features.
- **Model**: Utilize `gemini-3.1-pro-preview` to leverage high-performance reasoning and native RAG support.
- **Reasoning**: Enable `thinking_config` to improve the agent's ability to synthesize information from multiple document segments.
- **Configuration**: Hardcode the target RAG corpus ID initially, with an option to pass it via environment variables or constructor for flexibility.

## Risks / Trade-offs

- **[Risk]** API Rate Limiting → **[Mitigation]** Design the agent to handle common API exceptions and suggest retries if necessary.
- **[Risk]** Response Latency → **[Mitigation]** Implement streaming support so that partial results can be displayed as they are generated.
- **[Risk]** Hallucination despite RAG → **[Mitigation]** Use a high-level `thinking_config` and a very strict system prompt that explicitly forbids outside knowledge.
