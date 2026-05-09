output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "location" {
  description = "The Vertex AI location"
  value       = var.region
}

output "ui_service_url" {
  description = "The URL of the Cloud Run service"
  value       = google_cloud_run_v2_service.ui_service.uri
}
