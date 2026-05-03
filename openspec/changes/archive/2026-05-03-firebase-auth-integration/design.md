## Context

The current StewardshipAI application uses a simulated authentication system that is not suitable for deployment. We are transitioning to a real authentication flow using Google Cloud Identity Platform (Firebase Auth) to provide secure, production-ready access control for an internal group of developers.

## Goals / Non-Goals

**Goals:**
- Replace simulated auth with real Google SSO.
- Implement server-side JWT verification.
- Automate Identity Platform configuration via Terraform.
- Enable user-identified interaction logging.
- Maintain a $0 cost footprint (Spark/Free tier).

**Non-Goals:**
- Supporting multiple identity providers (only Google SSO).
- Implementing a full User Management UI.
- Deploying a Load Balancer (IAP is out of scope for cost reasons).

## Decisions

### 1. Identity Provider: Identity Platform (Firebase)
We will use Google Cloud Identity Platform. It is fully integrated with GCP and has a free tier for the first 50,000 monthly active users.
*   **Alternative Considered**: Identity-Aware Proxy (IAP). Rejected due to the ~$20/month requirement for an HTTPS Load Balancer.

### 2. Backend Verification: Firebase Admin SDK
We will use the `firebase-admin` Python library to verify ID Tokens on the backend.
*   **Rationale**: This ensures that even if the frontend is compromised, the backend will only accept valid, Google-signed tokens.

### 3. Frontend Integration: Custom Streamlit Component
Since Streamlit is server-side, we need a way to execute the Firebase JavaScript SDK in the user's browser. We will use a lightweight custom component or a standard community component (e.g., `streamlit-firebase-auth`) to handle the Google Login redirect and return the JWT to Python.

### 4. Configuration: Environment Variables
Firebase configuration (API Key, Auth Domain) will be delivered via environment variables.
*   **Rationale**: Simplifies deployment across local and Cloud Run environments without hardcoding secrets.

## Risks / Trade-offs

- **[Risk]** Streamlit session persistence can be tricky with Iframe-based auth components.
  - **Mitigation**: We will store the verified user email in `st.session_state` and ensure the token is re-verified if the session is cleared.
- **[Risk]** Local testing requires a valid Firebase configuration.
  - **Mitigation**: We will provide a dummy/test project setup guide for developers to use locally.

## Migration Plan

1.  Enable Identity Platform in the GCP Console.
2.  Update Terraform to reflect the new infrastructure.
3.  Update `config.py` to handle new environment variables.
4.  Refactor `app.py` to integrate the auth component.
5.  Verify the flow locally using a test Firebase project.
