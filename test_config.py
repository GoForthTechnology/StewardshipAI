import os
import pytest
from config import GCPConfig, get_config
from pydantic import ValidationError

def test_config_from_env_valid(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "test-project")
    monkeypatch.setenv("GCP_LOCATION", "us-south1")
    monkeypatch.setenv("GCP_RAG_CORPUS_ID", "test-corpus")
    monkeypatch.setenv("FIREBASE_API_KEY", "test-api-key")
    
    config = get_config()
    assert config.project_id == "test-project"
    assert config.location == "us-south1"
    assert config.rag_corpus_id == "test-corpus"
    assert config.firebase_api_key == "test-api-key"

def test_config_missing_required(monkeypatch):
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    monkeypatch.delenv("GCP_PROJECT", raising=False)
        
    with pytest.raises(ValueError, match="GCP_PROJECT_ID or GCP_PROJECT is required"):
        get_config()

def test_firebase_config_fields(monkeypatch):
    monkeypatch.setenv("FIREBASE_DATABASE_URL", "https://test.firebaseio.com")
    monkeypatch.setenv("FIREBASE_STORAGE_BUCKET", "test.appspot.com")
    
    config = GCPConfig.from_env()
    assert config.firebase_database_url == "https://test.firebaseio.com"
    assert config.firebase_storage_bucket == "test.appspot.com"
