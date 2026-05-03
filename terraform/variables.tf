variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-south1"
}

variable "rag_corpus_name" {
  description = "The name of the RAG corpus"
  type        = string
  default     = "stewardship-ai-corpus"
}

variable "rag_corpus_description" {
  description = "Description of the RAG corpus"
  type        = string
  default     = "Corpus for StewardshipAI research documents"
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
