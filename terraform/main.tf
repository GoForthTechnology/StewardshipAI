resource "google_vertex_ai_rag_engine_config" "default" {
  project = var.project_id
  region  = var.region

  rag_managed_db_config {
    basic {}
  }
}

resource "google_vertex_ai_rag_corpus" "stewardship_corpus" {
  display_name = var.rag_corpus_name
  description  = var.rag_corpus_description
  region       = var.region

  # Optional: Explicitly define the embedding model
  # If omitted, it defaults to the latest text-embedding model
  embedding_model_config {
    publisher_model = "projects/${var.project_id}/locations/${var.region}/publishers/google/models/text-embedding-004"
  }

  depends_on = [google_vertex_ai_rag_engine_config.default]
}

data "google_project" "project" {}

resource "google_storage_bucket_iam_member" "rag_agent_reader" {
  bucket = var.document_bucket_name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-vertex-rag.iam.gserviceaccount.com"
}

resource "google_service_account" "ui_service_account" {
  account_id   = "stewardship-ai-ui-sa"
  display_name = "StewardshipAI UI Service Account"
}

resource "google_project_iam_member" "ui_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ui_service_account.email}"
}

resource "google_cloud_run_v2_service" "ui_service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.ui_service_account.email
    containers {
      image = var.container_image
      
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "GCP_LOCATION"
        value = var.region
      }
      env {
        name  = "GCP_RAG_CORPUS_ID"
        value = google_vertex_ai_rag_corpus.stewardship_corpus.name
      }
    }
  }

  depends_on = [google_project_iam_member.ui_ai_user]
}

resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.ui_service.location
  name     = google_cloud_run_v2_service.ui_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
