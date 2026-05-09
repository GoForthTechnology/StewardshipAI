import os
from pydantic import BaseModel, Field, ValidationError

class GCPConfig(BaseModel):
    project_id: str
    location: str
    rag_corpus_id: str
    diocese_name: str = "Stewardship AI Portal"
    api_key: str | None = None
    firebase_api_key: str | None = None
    firebase_auth_domain: str | None = None
    firebase_database_url: str | None = None
    firebase_storage_bucket: str | None = None
    firebase_messaging_sender_id: str | None = None
    firebase_app_id: str | None = None
    firebase_measurement_id: str | None = None

    @classmethod
    def from_env(cls):
        """Creates a GCPConfig object from environment variables."""
        return cls(
            project_id=os.environ.get("GCP_PROJECT_ID", os.environ.get("GCP_PROJECT", "")),
            location=os.environ.get("GCP_LOCATION", "us-south1"),
            rag_corpus_id=os.environ.get("GCP_RAG_CORPUS_ID", os.environ.get("GCP_RAG_CORPUS", "")),
            diocese_name=os.environ.get("DIOCESE_NAME", "Stewardship AI Portal"),
            api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
            firebase_api_key=os.environ.get("FIREBASE_API_KEY"),
            firebase_auth_domain=os.environ.get("FIREBASE_AUTH_DOMAIN"),
            firebase_database_url=os.environ.get("FIREBASE_DATABASE_URL"),
            firebase_storage_bucket=os.environ.get("FIREBASE_STORAGE_BUCKET"),
            firebase_messaging_sender_id=os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
            firebase_app_id=os.environ.get("FIREBASE_APP_ID"),
            firebase_measurement_id=os.environ.get("FIREBASE_MEASUREMENT_ID")
        )

def get_config() -> GCPConfig:
    """Helper to get and validate the configuration."""
    try:
        config = GCPConfig.from_env()
        # Validation for required fields (since default is "" if missing)
        if not config.project_id:
            raise ValueError("GCP_PROJECT_ID or GCP_PROJECT is required")
        if not config.rag_corpus_id:
            raise ValueError("GCP_RAG_CORPUS_ID or GCP_RAG_CORPUS is required")
        return config
    except (ValidationError, ValueError) as e:
        print(f"Configuration Error: {e}")
        raise
