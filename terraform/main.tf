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
