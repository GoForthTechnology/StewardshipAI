import os
import pytest
from config import GCPConfig, get_config
from pydantic import ValidationError

def test_config_from_env_valid():
    os.environ["GCP_PROJECT_ID"] = "test-project"
    os.environ["GCP_LOCATION"] = "us-south1"
    os.environ["GCP_RAG_CORPUS_ID"] = "test-corpus"
    os.environ["FIREBASE_API_KEY"] = "test-api-key"
    
    config = get_config()
    assert config.project_id == "test-project"
    assert config.location == "us-south1"
    assert config.rag_corpus_id == "test-corpus"
    assert config.firebase_api_key == "test-api-key"

def test_config_missing_required():
    if "GCP_PROJECT_ID" in os.environ:
        del os.environ["GCP_PROJECT_ID"]
    if "GCP_PROJECT" in os.environ:
        del os.environ["GCP_PROJECT"]
        
    with pytest.raises(ValueError, match="GCP_PROJECT_ID or GCP_PROJECT is required"):
        get_config()

def test_firebase_config_fields():
    os.environ["FIREBASE_DATABASE_URL"] = "https://test.firebaseio.com"
    os.environ["FIREBASE_STORAGE_BUCKET"] = "test.appspot.com"
    
    config = GCPConfig.from_env()
    assert config.firebase_database_url == "https://test.firebaseio.com"
    assert config.firebase_storage_bucket == "test.appspot.com"
