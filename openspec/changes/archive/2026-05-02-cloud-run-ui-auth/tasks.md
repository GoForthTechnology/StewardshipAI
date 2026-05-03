## 1. Firebase and Infrastructure Setup

- [x] 1.1 Enable Identity Platform/Firebase Auth in the GCP console.
- [x] 1.2 Configure Google as a sign-in provider and set authorized domains.
- [x] 1.3 Add Cloud Run and IAM definitions to `terraform/main.tf`.

## 2. Web UI Development

- [x] 2.1 Create `app.py` with Streamlit basic chat structure.
- [x] 2.2 Integrate Firebase Auth redirect/verification logic in `app.py`.
- [x] 2.3 Implement the authorized email allow-list check.
- [x] 2.4 Connect `app.py` to the existing `GCPRagAgent` and display citations.

## 3. Containerization and Deployment

- [x] 3.1 Create a lean `Dockerfile` for the Streamlit application.
- [x] 3.2 Build and push the container image to Artifact Registry.
- [x] 3.3 Deploy the service to Cloud Run and verify the authenticated flow.
