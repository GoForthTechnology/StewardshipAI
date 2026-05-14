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

output "wif_provider_name" {
  description = "The full resource name of the Workload Identity Provider for GitHub Actions"
  value       = "projects/${data.google_project.project.number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_pool.workload_identity_pool_id}/providers/${google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id}"
}

output "apphub_application_id" {
  description = "The ID of the App Hub application"
  value       = google_apphub_application.stewardship_portal.application_id
}
