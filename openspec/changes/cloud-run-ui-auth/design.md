## Context

The current agent is a CLI-based Python script. While functional for development, it requires users to have Python and GCP credentials configured locally. To share the agent with non-technical testers, we need a hosted web interface that handles authentication centrally.

## Goals / Non-Goals

**Goals:**
- Deploy a responsive Streamlit UI to Google Cloud Run.
- Implement "Sign in with Google" via Firebase Authentication.
- Restrict access to a pre-defined list of authorized Gmail addresses.
- Maintain the existing RAG capabilities while surfacing citations in the UI.

**Non-Goals:**
- Implementing a custom user database (relying on Firebase/Google).
- Building a complex multi-page dashboard (single-page chat is sufficient).
- Automated CI/CD (manual deployment via Terraform/CLI for this phase).

## Decisions

- **Framework**: **Streamlit** was chosen for the UI due to its high development speed and native Python support, allowing us to reuse the existing `rag_agent.py` logic directly.
- **Hosting**: **Google Cloud Run** was chosen for its "Scale-to-Zero" capability, which minimizes costs during inactive periods.
- **Authentication**: **Firebase Authentication (Identity Platform)** will be used to provide secure Google SSO without the $20/month overhead of a Global Load Balancer + IAP.
- **Identity Enforcement**: The app will verify the user's email address against an `AUTHORIZED_USERS` environment variable or a local config file.

## Risks / Trade-offs

- **[Risk]** Streamlit state management complexity → **[Mitigation]** Use `st.session_state` to track chat history and authentication tokens consistently.
- **[Risk]** Cold start latency → **[Mitigation]** Keep the Docker image lean by using `python:3.11-slim` and minimal dependencies.
- **[Trade-off]** Firebase client-side auth in Streamlit → **[Rationale]** Since Streamlit isn't a traditional frontend/backend split, we will use a custom component or redirect flow to handle the Firebase JWT verification.
