## 1. Backend Implementation (FastAPI)

- [x] 1.1 Add FastAPI and Uvicorn to `requirements.txt`.
- [x] 1.2 Create `api.py` to initialize the FastAPI app and configure CORS.
- [x] 1.3 Implement Firebase JWT verification middleware/dependency in `api.py`.
- [x] 1.4 Create a POST `/chat` endpoint in `api.py` that accepts a prompt and persona, then streams the RAG agent response.
- [x] 1.5 Implement dynamic `/config.js` endpoint to serve Firebase credentials at runtime.

## 2. Frontend Setup (Angular)

- [x] 2.1 Initialize a new Angular project in a `frontend/` directory using `ng new`.
- [x] 2.2 Configure Tailwind CSS v4 using explicit CLI compilation in the build process.
- [x] 2.3 Install Firebase SDK, `@angular/fire`, and `zone.js` in the project and configure them.

## 3. Frontend Implementation (Authentication & Layout)

- [x] 3.1 Implement a `Login` component using Firebase Auth (Google Sign-In).
- [x] 3.2 Create the main layout component with a deep blue sidebar and cream main area.
- [x] 3.3 Implement the persona toggle (Priest/Parishioner) using an Angular service for state.

## 4. Frontend Implementation (Chat Interface)

- [x] 4.1 Implement the "Quick-Start" discovery grid component.
- [x] 4.2 Build the chat interface (message components, input component).
- [x] 4.3 Implement a `ChatService` to handle the FastAPI `/chat` stream using `Fetch API` or `SSE`.
- [x] 4.4 Render citations and handle persona-specific content in the UI.

## 5. Cleanup & Deployment

- [x] 5.1 Remove `app.py` and the Streamlit dependency.
- [x] 5.2 Update `Dockerfile` to build the Angular app and serve the static files alongside FastAPI.
- [x] 5.3 Update `run_local.sh` to support the new stack.
