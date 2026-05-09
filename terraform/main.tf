data "google_project" "project" {}

resource "google_service_account" "ui_service_account" {
  account_id   = "stewardship-ai-ui-sa"
  display_name = "StewardshipAI UI Service Account"
}

resource "google_project_iam_member" "ui_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ui_service_account.email}"
}

resource "google_project_iam_member" "ui_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.ui_service_account.email}"
}

resource "google_project_iam_member" "ui_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.ui_service_account.email}"
}

resource "google_project_iam_member" "ui_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.ui_service_account.email}"
}

resource "google_project_service" "identity_platform" {
  project = var.project_id
  service = "identitytoolkit.googleapis.com"
}

resource "google_project_service" "firebase_hosting" {
  project = var.project_id
  service = "firebasehosting.googleapis.com"
}

resource "google_identity_platform_config" "default" {
  project = var.project_id
  
  authorized_domains = [
    "localhost",
    "${var.project_id}.firebaseapp.com",
    "${var.project_id}.web.app",
    "stewardship.goforthtech.org",
  ]

  depends_on = [google_project_service.identity_platform]
}

resource "google_identity_platform_default_supported_idp_config" "google_idp" {
  project    = var.project_id
  enabled    = true
  idp_id     = "google.com"
  client_id  = var.google_client_id
  client_secret = var.google_client_secret
  
  depends_on = [google_identity_platform_config.default]
}

resource "google_firebase_hosting_site" "stewardship_portal" {
  provider = google-beta
  project  = var.project_id
  site_id  = "stewardship-portal"

  depends_on = [google_project_service.firebase_hosting]
}

resource "google_firebase_hosting_version" "v1" {
  provider = google-beta
  site_id  = google_firebase_hosting_site.stewardship_portal.site_id
  config {
    rewrites {
      glob = "**"
      run {
        service_id = google_cloud_run_v2_service.ui_service.name
        region     = var.region
      }
    }
  }
}

resource "google_firebase_hosting_release" "v1" {
  provider     = google-beta
  site_id      = google_firebase_hosting_site.stewardship_portal.site_id
  version_name = google_firebase_hosting_version.v1.name
  message      = "Initial Cloud Run rewrite"
}

resource "google_firebase_hosting_custom_domain" "stewardship_domain" {
  provider      = google-beta
  project       = var.project_id
  site_id       = google_firebase_hosting_site.stewardship_portal.site_id
  custom_domain = "stewardship.goforthtech.org"
}

resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = "stewardship-ai"
  description   = "Docker repository for StewardshipAI"
  format        = "DOCKER"

  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 5
    }
  }

  cleanup_policies {
    id     = "delete-old-untagged"
    action = "DELETE"
    condition {
      tag_state  = "UNTAGGED"
      older_than = "86400s" # 1 day
    }
  }
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
        value = var.rag_corpus_id
      }
      env {
        name  = "GCP_MAGISTERIUM_CORPUS_ID"
        value = var.magisterium_corpus_id
      }
      env {
        name  = "FIREBASE_API_KEY"
        value = var.firebase_api_key
      }
      env {
        name  = "FIREBASE_AUTH_DOMAIN"
        value = var.firebase_auth_domain
      }
      env {
        name  = "FIREBASE_STORAGE_BUCKET"
        value = var.firebase_storage_bucket
      }
      env {
        name  = "FIREBASE_APP_ID"
        value = var.firebase_app_id
      }
      env {
        name  = "FIREBASE_MESSAGING_SENDER_ID"
        value = var.firebase_messaging_sender_id
      }
      env {
        name  = "FIREBASE_MEASUREMENT_ID"
        value = var.firebase_measurement_id
      }
      env {
        name  = "DIOCESE_NAME"
        value = var.diocese_name
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

# --- GitHub Actions Workload Identity Federation ---

resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
  description              = "Identity pool for GitHub Actions deployments"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }
  attribute_condition = "assertion.repository == 'GoForthTechnology/StewardshipAI'"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "wif_impersonation" {
  service_account_id = google_service_account.ui_service_account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/GoForthTechnology/StewardshipAI"
}
