## Context

The Stewardship Portal currently uses Streamlit (`app.py`), which tightly couples the UI and the backend. While Streamlit was excellent for prototyping, it has severe limitations regarding custom styling, responsive design, and complex client-side interactions (like modern OAuth flows). To deliver a high-quality, branded experience for the Diocese, we are shifting to a decoupled architecture: an Angular frontend and a FastAPI backend.

## Goals / Non-Goals

**Goals:**
- Create a new REST API using FastAPI to serve the `GCPRagAgent`.
- Implement token-based authentication (Firebase JWT) in FastAPI.
- Build a new Angular application for the frontend.
- Maintain all existing "Stewardship Guide" prompt behaviors and persona switching.

**Non-Goals:**
- Modifying the underlying RAG infrastructure or Google Cloud project setup.
- Adding database persistence for chat history (sessions will remain ephemeral).

## Decisions

- **FastAPI for Backend**: FastAPI is lightweight, supports async Python inherently, and is easy to serve alongside our existing `rag_agent.py` code. We will replace `app.py` with `api.py`.
- **Angular for Frontend**: Angular provides a robust, opinionated framework that is ideal for building enterprise-grade applications. We will use Angular components and services to manage the portal's state and UI.
- **Angular CLI**: We will use the Angular CLI (`ng new`) to scaffold the project.
- **Client-Side Firebase Auth**: The Angular app will use the `@angular/fire` library or the standard Firebase JS SDK to handle the Google SSO flow. It will then pass the resulting ID token to the FastAPI backend via the `Authorization: Bearer <token>` header.
- **Streaming Strategy**: FastAPI will stream responses back to the Angular client using Server-Sent Events (SSE). The Angular client will use a `ReadableStream` reader or the `EventSource` API to process the incoming chunks in real-time.
- **Dynamic Runtime Configuration**: To avoid rebuilding the Angular app for different environments (local vs. Cloud Run), the FastAPI backend serves a `/config.js` file that injects Firebase credentials into the `window.ENV` object.
- **Tailwind v4 Build Strategy**: Due to integration complexities with the Angular bundler, we use `@tailwindcss/cli` to explicitly pre-compile styles into `styles.compiled.css` during the Docker build process.

## Risks / Trade-offs

- **[Risk] CORS Issues** → **Mitigation**: Configure FastAPI's `CORSMiddleware` to explicitly allow the Angular app's local development port (e.g., `http://localhost:4200`) and the production domain.
- **[Trade-off] Increased Complexity** → **Rationale**: Managing two separate codebases (Angular and Python) requires more boilerplate and build steps than a single Streamlit script, but it is the only way to achieve the required UI fidelity.
