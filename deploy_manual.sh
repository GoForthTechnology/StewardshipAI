#!/bin/bash

# deploy_manual.sh - Orchestrate manual deployment to Cloud Run

set -e

# 1. Parse arguments
SKIP_BUILD=false
if [[ "$1" == "--skip-build" ]]; then
    SKIP_BUILD=true
fi

# 2. Source local environment
if [ -f "setup_env.sh" ]; then
    echo "--- Sourcing environment variables from setup_env.sh ---"
    source setup_env.sh
else
    echo "Error: setup_env.sh not found. Please create it first."
    exit 1
fi

# 2. Validation
if [ -z "$GCP_PROJECT_ID" ] || [ -z "$GCP_LOCATION" ]; then
    echo "Error: GCP_PROJECT_ID and GCP_LOCATION must be set in setup_env.sh"
    exit 1
fi

if [[ "$GCP_PROJECT_ID" =~ ^[0-9]+$ ]]; then
    echo "Error: GCP_PROJECT_ID appears to be a project number ($GCP_PROJECT_ID)."
    echo "Please use the alphanumeric slug (e.g., 'stewardship-ai') instead."
    exit 1
fi

IMAGE_NAME="${GCP_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/stewardship-ai/app:latest"

echo "--- Deployment Configuration ---"
echo "Project: $GCP_PROJECT_ID"
echo "Region:  $GCP_LOCATION"
echo "Image:   $IMAGE_NAME"
echo "--------------------------------"

# 3. Ensure Artifact Registry exists
echo "--- Ensuring Artifact Registry repository exists ---"
gcloud artifacts repositories describe stewardship-ai --location="$GCP_LOCATION" > /dev/null 2>&1 || \
gcloud artifacts repositories create stewardship-ai \
    --repository-format=docker \
    --location="$GCP_LOCATION" \
    --description="Docker repository for StewardshipAI"

# 4. Build and Push to Artifact Registry
if [ "$SKIP_BUILD" = false ]; then
    echo "--- Building and Pushing Image ---"
    gcloud builds submit --tag "$IMAGE_NAME" .
else
    echo "--- Skipping Build (using existing image: $IMAGE_NAME) ---"
fi

# 5. Generate tfvars
echo "--- Generating terraform/deploy.tfvars ---"
cat <<EOF > terraform/deploy.tfvars
project_id                   = "$GCP_PROJECT_ID"
region                       = "$GCP_LOCATION"
container_image              = "$IMAGE_NAME"
rag_corpus_id                = "$GCP_RAG_CORPUS_ID"
document_bucket_name         = "stewardship-ai-docs-${GCP_PROJECT_ID}"
firebase_api_key             = "$FIREBASE_API_KEY"
firebase_auth_domain         = "$FIREBASE_AUTH_DOMAIN"
firebase_storage_bucket      = "$FIREBASE_STORAGE_BUCKET"
firebase_app_id              = "$FIREBASE_APP_ID"
firebase_messaging_sender_id = "$FIREBASE_MESSAGING_SENDER_ID"
firebase_measurement_id      = "$FIREBASE_MEASUREMENT_ID"
diocese_name                 = "$DIOCESE_NAME"
google_client_id             = "$GOOGLE_CLIENT_ID"
google_client_secret         = "$GOOGLE_CLIENT_SECRET"
EOF

# 5. Terraform Plan & Apply
echo "--- Initializing Terraform ---"
cd terraform
terraform init

echo "--- Terraform Plan ---"
terraform plan -var-file="deploy.tfvars"

read -p "Do you want to apply these changes to GCP? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "--- Applying Changes ---"
    terraform apply -var-file="deploy.tfvars" -auto-approve
    echo "--- Deployment Complete ---"
else
    echo "Deployment cancelled."
fi
