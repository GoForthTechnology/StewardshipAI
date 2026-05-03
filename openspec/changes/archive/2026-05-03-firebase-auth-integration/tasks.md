## 1. Infrastructure & Config

- [x] 1.1 Update `terraform/main.tf` to enable Identity Platform and configure Google as a provider.
- [x] 1.2 Add Firebase configuration variables to `terraform/variables.tf`.
- [x] 1.3 Update `config.py` to include `FirebaseConfig` and load it from environment variables.
- [x] 1.4 Update `setup_env.sh.template` with placeholders for Firebase configuration.

## 2. Authentication Logic

- [x] 2.1 Initialize Firebase Admin SDK in `app.py`.
- [x] 2.2 Replace simulated login with a Firebase Google SSO component.
- [x] 2.3 Implement token verification logic in `app.py`.
- [x] 2.4 Update the authorized email allow-list check to use verified identities.

## 3. Agent & Auditing

- [x] 3.1 Update `rag_agent.py` to accept `user_email` in the `generate_response` method.
- [x] 3.2 Implement interaction logging (audit trails) for each agent response.
- [x] 3.3 Ensure the user identity is propagated to the generative model context.

## 4. Local Verification

- [x] 4.1 Build the updated Docker image with new dependencies.
- [x] 4.2 Run the container locally with a test Firebase configuration.
- [x] 4.3 Verify that the simulated login is gone and real Google SSO is active.
