output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "location" {
  description = "The Vertex AI location"
  value       = var.region
}

output "rag_corpus_id" {
  description = "The full resource ID of the RAG corpus"
  value       = google_vertex_ai_rag_corpus.stewardship_corpus.name
}
