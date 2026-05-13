#!/bin/bash

# run_local.sh - Helper script to run StewardshipAI Docker container locally

# 1. Source the environment variables
if [ -f "setup_env.sh" ]; then
    echo "--- Sourcing environment variables from setup_env.sh ---"
    source setup_env.sh
else
    echo "Error: setup_env.sh not found. Please create it first."
    exit 1
fi

# 2. Define local ADC path
ADC_PATH="$HOME/.config/gcloud/application_default_credentials.json"

if [ ! -f "$ADC_PATH" ]; then
    echo "Error: Application Default Credentials (ADC) not found at $ADC_PATH"
    echo "Please run: gcloud auth application-default login"
    exit 1
fi

echo "--- Starting StewardshipAI Container ---"
echo "Project ID: $GCP_PROJECT_ID"
echo "Location:   $GCP_LOCATION"
echo "URL:        http://localhost:8080"
echo "---------------------------------------"

docker run -it --rm \
  -p 8080:8080 \
  -e GCP_PROJECT_ID="$GCP_PROJECT_ID" \
  -e GOOGLE_CLOUD_PROJECT="$GCP_PROJECT_ID" \
  -e GCP_LOCATION="$GCP_LOCATION" \
  -e GCP_RAG_CORPUS_ID="$GCP_RAG_CORPUS_ID" \
  -e GCP_MAGISTERIUM_CORPUS_ID="$GCP_MAGISTERIUM_CORPUS_ID" \
  -e FIREBASE_API_KEY="$FIREBASE_API_KEY" \
  -e FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN" \
  -e FIREBASE_DATABASE_URL="$FIREBASE_DATABASE_URL" \
  -e FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET" \
  -e FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID" \
  -e FIREBASE_APP_ID="$FIREBASE_APP_ID" \
  -e FIREBASE_MEASUREMENT_ID="$FIREBASE_MEASUREMENT_ID" \
  -e DIOCESE_NAME="$DIOCESE_NAME" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/adc.json \
  -v "$ADC_PATH":/tmp/keys/adc.json:ro \
  stewardship-ai
