import os
from pydantic import BaseModel, Field, ValidationError

class GCPConfig(BaseModel):
    project_id: str
    location: str
    rag_corpus_id: str
    api_key: str | None = None

    @classmethod
    def from_env(cls):
        """Creates a GCPConfig object from environment variables."""
        return cls(
            project_id=os.environ.get("GCP_PROJECT_ID", os.environ.get("GCP_PROJECT", "")),
            location=os.environ.get("GCP_LOCATION", "us-south1"),
            rag_corpus_id=os.environ.get("GCP_RAG_CORPUS_ID", os.environ.get("GCP_RAG_CORPUS", "")),
            api_key=os.environ.get("GOOGLE_CLOUD_API_KEY")
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
