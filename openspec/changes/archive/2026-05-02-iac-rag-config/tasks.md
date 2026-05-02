## 1. Terraform Setup

- [x] 1.1 Create a `terraform` directory in the project root.
- [x] 1.2 Define the main Terraform configuration for Vertex AI RAG resources.
- [x] 1.3 Add GCS bucket variable and IAM role binding for the RAG Service Agent in Terraform.
- [x] 1.4 Implement Terraform outputs for project ID, location, and RAG corpus ID.

## 2. Agent Refactoring

- [x] 2.1 Update `config.py` to ensure it correctly handles resource identifiers provided by Terraform.
- [x] 2.2 Verify that the `GCPRagAgent` can successfully initialize using the outputs from the Terraform provisioning.

## 3. Documentation and Verification

- [x] 3.1 Provide a `README.md` within the `terraform` directory explaining the provisioning process.
- [x] 3.2 Verify the end-to-end flow: Provision infrastructure -> Run agent -> Grounded response.
