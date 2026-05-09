variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-south1"
}

variable "rag_corpus_id" {
  description = "The full resource name of the RAG corpus (from setup_env.sh)"
  type        = string
}

variable "document_bucket_name" {
  description = "The name of the GCS bucket containing the source documents"
  type        = string
}

variable "service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "stewardship-ai-ui"
}

variable "container_image" {
  description = "The Docker image to deploy to Cloud Run"
  type        = string
  default     = "gcr.io/cloudrun/hello" # Placeholder until first build
}

variable "firebase_api_key" {
  description = "The Firebase API Key for frontend authentication"
  type        = string
  sensitive   = true
}

variable "firebase_auth_domain" {
  description = "The Firebase Auth Domain for frontend authentication"
  type        = string
}

variable "firebase_storage_bucket" {
  description = "The Firebase Storage Bucket"
  type        = string
}

variable "firebase_app_id" {
  description = "The Firebase App ID"
  type        = string
}

variable "firebase_messaging_sender_id" {
  description = "The Firebase Messaging Sender ID"
  type        = string
  default     = ""
}

variable "firebase_measurement_id" {
  description = "The Firebase Measurement ID"
  type        = string
  default     = ""
}

variable "diocese_name" {
  description = "The name of the diocese"
  type        = string
  default     = "Catholic Diocese of Wichita"
}

variable "google_client_id" {
  description = "The Google OAuth Client ID for Identity Platform"
  type        = string
}

variable "google_client_secret" {
  description = "The Google OAuth Client Secret for Identity Platform"
  type        = string
  sensitive   = true
}
