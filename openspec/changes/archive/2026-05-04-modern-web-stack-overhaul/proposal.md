## Why

The current Streamlit-based UI for the Stewardship Portal faces significant styling and layout limitations that prevent us from delivering a high-fidelity, deeply branded experience. To create a polished, robust, and truly pastoral digital experience for the Diocese of Wichita, we need to decouple the frontend from the backend by transitioning to a modern web stack (Angular) and a dedicated API (FastAPI).

## What Changes

- **BREAKING**: Remove the Streamlit application (`app.py`).
- **New API Backend**: Introduce a FastAPI application that wraps the `GCPRagAgent` and exposes a `/chat` endpoint.
- **New Angular Frontend**: Build a new frontend using Angular to implement the "Stewardship Portal" with full control over the UI, branding, and layout.
- **Client-Side Authentication**: Migrate Firebase Google SSO logic to the Angular frontend, passing authentication tokens to the FastAPI backend for verification.

## Capabilities

### New Capabilities
- `api-backend`: A new FastAPI application that exposes the RAG agent capabilities via REST endpoints and handles JWT token verification.

### Modified Capabilities
- `web-interface`: Complete rewrite of the web interface using Angular to support advanced styling, responsive layouts, and a dedicated UI for persona selection and quick-start actions.
- `user-authentication`: Authentication flow shifts to a standard client-server model where the Angular app handles the Firebase Google login and sends the ID token in the `Authorization` header to the FastAPI backend.

## Impact

- Removes Streamlit dependency and `app.py`.
- Introduces new `package.json` and a `frontend/` directory for the Angular application.
- Introduces `api.py` (FastAPI) to replace the Streamlit routing.
- The `GCPRagAgent` class remains largely untouched, preserving the core RAG logic and prompts.
- Deployment (Dockerfile/Cloud Run) will need to be updated to serve both the static React build and the FastAPI endpoints, or run them as separate services (a combined approach is simpler for now).
