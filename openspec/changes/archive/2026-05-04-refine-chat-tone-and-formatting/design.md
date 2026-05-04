## Context

The current `SYSTEM_INSTRUCTION` in `rag_agent.py` uses placeholders like `{user_email}` which results in responses greeting the user by their full email address (e.g., "Hello parkeroth@gmail.com"). Furthermore, the instructions for the "Stewardship Guide" persona encourage a "warm and encouraging" tone that has drifted into being overly verbose and "pandering". The frontend renders markdown, but without proper spacing rules in the prompt or CSS in the frontend, long lists can look cluttered.

## Goals / Non-Goals

**Goals:**
- Remove raw email addresses from the agent's conversational output.
- Refactor the system prompt to enforce a more professional, concise, and direct pastoral tone.
- Standardize markdown output (e.g., mandatory double newlines between list items and paragraphs) for better readability.
- Fix UI rendering issues for markdown lists in the Angular frontend.

**Non-Goals:**
- Removing the `user_email` from logs or the backend; it remains essential for auditing.
- Changing the underlying RAG grounding logic.

## Decisions

- **Prompt-Based Identity Handling**: Instead of greeting by email, the agent will be instructed to speak to the user based on their selected persona (e.g., "Dear Parishioner" or simply "Welcome") or avoid a formal name/email greeting entirely.
- **Tone "Tightening"**: We will update the `SYSTEM_INSTRUCTION` to prioritize "pastoral clarity" over "flowery encouragement". We will explicitly forbid repetitive phrases like "It's wonderful to talk about stewardship!".
- **Markdown Formatting Rules**: We will add a specific rule to the `SYSTEM_INSTRUCTION` requiring double newlines for paragraph and list item separation to ensure the Angular markdown parser renders them with enough white space.
- **Frontend Styling**: We will update `frontend/src/styles.css` to add consistent padding and margins for `ul`, `ol`, and `li` tags within the chat message container.

## Risks / Trade-offs

- **[Risk] Tone becoming too cold** → **Mitigation**: We will retain terms like "Stewardship Guide" and the core mission, focusing only on removing the "pandering" elements.
- **[Trade-off] Increased prompt complexity** → **Rationale**: Explicitly defining formatting rules in the prompt is more reliable than hoping the model defaults to the user's preferred layout.
