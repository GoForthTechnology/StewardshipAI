# Vertex AI RAG Infrastructure (Terraform)

This directory contains Terraform configuration to provision the necessary infrastructure for the StewardshipAI research agent.

## Resources Provisioned

- **Vertex AI RAG Engine Config**: Configures the managed vector database.
- **Vertex AI RAG Corpus**: The index where documents are stored and searched.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed.
- GCP credentials configured (e.g., via `gcloud auth application-default login`).
- Vertex AI API enabled in your GCP project.

## Usage

1.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

2.  **Plan the infrastructure**:
    ```bash
    terraform plan -var="project_id=your-project-id" -var="document_bucket_name=your-bucket-name"
    ```

3.  **Apply the configuration**:
    ```bash
    terraform apply -var="project_id=your-project-id" -var="document_bucket_name=your-bucket-name"
    ```

4.  **Capture Outputs**:
    The command will output the `rag_corpus_id`. Use this value to set your environment variables for the agent.

## Environment Integration

After provisioning, you can set your environment variables using the Terraform outputs:

```bash
export GCP_PROJECT_ID=$(terraform output -raw project_id)
export GCP_LOCATION=$(terraform output -raw location)
export GCP_RAG_CORPUS_ID=$(terraform output -raw rag_corpus_id)
```
