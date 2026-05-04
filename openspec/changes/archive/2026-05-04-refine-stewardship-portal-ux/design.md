## Context

The StewardshipAI agent currently uses a generic "Strict Research Assistant" persona. This change refactors the agent to act as a "Stewardship Guide" for the Catholic Diocese of Wichita. The project is built with Python, Streamlit, and Vertex AI RAG.

## Goals / Non-Goals

**Goals:**
- Implement a warm, pastoral persona in the system prompt.
- Tailor agent behavior based on user role (Priest vs. Parishioner).
- Apply custom branding to the Streamlit UI.
- Add discovery elements (quick-start buttons) to improve user engagement.

**Non-Goals:**
- Moving to a multi-page app architecture.
- Implementing persistent chat history (beyond current session).
- Changing the underlying RAG infrastructure or authentication flow.

## Decisions

- **Dynamic System Prompting**: The `SYSTEM_INSTRUCTION` in `rag_agent.py` will be converted into a template that incorporates both the `user_email` and the user's selected `persona`. This allows the agent to switch tone and focus dynamically without re-initializing the class.
- **Persona Context Injection**: The selected persona (e.g., "Parishioner") will be passed as a parameter to `generate_response`.
- **Branded UI Injection**: We will use Streamlit's `st.set_page_config` and `st.markdown` (with `unsafe_allow_html=True`) to inject a custom CSS theme that aligns with the Diocese of Wichita's branding (e.g., using specific hex codes for ecclesiastical colors like gold or deep blue).
- **Interactive Discovery Grid**: Instead of a blank landing page, the app will show a grid of buttons that pre-fill the chat input. We will use a "callback-less" pattern where clicking a button sets `st.session_state.discovery_prompt`, which then triggers the chat logic on the next rerun.

## Risks / Trade-offs

- **[Risk] Prompt Injection** → **[Mitigation]** The persona selection will be restricted to a hardcoded enum/list in the UI to prevent arbitrary text being injected into the system prompt.
- **[Risk] Hallucination due to Tone** → **[Mitigation]** The system instruction will maintain strict "Source Lockdown" and "Citation Enforcement" rules, explicitly stating that pastoral warmth does not permit inventing facts.
- **[Trade-off] Streamlit CSS Hacks** → **[Rationale]** Streamlit has limited native theming for deep customization. Injecting CSS is the fastest way to achieve a "portal" look without moving to a full-stack React/FastAPI setup.
