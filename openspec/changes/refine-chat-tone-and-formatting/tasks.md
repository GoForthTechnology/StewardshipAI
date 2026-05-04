## 1. Prompt Engineering (Python)

- [x] 1.1 Update `SYSTEM_INSTRUCTION` in `rag_agent.py` to remove the email greeting and enforce a more concise, professional tone.
- [x] 1.2 Add explicit markdown formatting rules (double newlines for lists and paragraphs) to the `SYSTEM_INSTRUCTION`.
- [x] 1.3 Refine the `PRIEST_INSTRUCTION` and `PARISHIONER_INSTRUCTION` to avoid flowery preamble.

## 2. Frontend Styling & Rendering (Angular)

- [x] 2.1 Update `frontend/src/app/app.css` or `styles.css` to add consistent padding and list-style-type for `ul`, `ol`, `li`, `p`, and `strong` elements.
- [x] 2.2 Install `marked` library and create a `MarkdownPipe` to handle secure HTML rendering of agent responses.
- [x] 2.3 Update `PortalComponent` to use `MarkdownPipe` and `innerHTML` for displaying chat content.

## 3. Verification

- [x] 3.1 Run `verify_rag.py` and inspect outputs to ensure no raw emails are present and the tone is more professional.
- [x] 3.2 Manually verify the chat interface to ensure list formatting, spacing, and bolding are working as expected.
