# StewardshipAI

StewardshipAI is a specialized research assistant agent powered by Google Cloud Vertex AI RAG Engine. It is designed to provide strictly grounded answers with citations based on a proprietary document corpus.

## Features

- **Grounded Research**: Answers are strictly limited to provided source material.
- **Citation Enforcement**: Every claim is cited to its source in the RAG corpus.
- **Platform Native**: Optimized for GCP deployment using Application Default Credentials (ADC).
- **Environment Driven**: Fully configurable via environment variables.

## Getting Started

### Prerequisites

- Python 3.10+
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- Access to the Vertex AI RAG corpus in your GCP project.

### Installation

```bash
python3 -m pip install google-genai pydantic
```

### Configuration

Set the following environment variables:

```bash
export GCP_PROJECT_ID="YOUR_PROJECT_ID"
export GCP_LOCATION="us-south1"
export GCP_RAG_CORPUS_ID="projects/YOUR_PROJECT_ID/locations/us-south1/ragCorpora/YOUR_CORPUS_ID"
```

### Authentication

**Recommended**: Use Application Default Credentials (ADC).
```bash
gcloud auth application-default login
```

**Alternative**: Use an API Key (not recommended for production).
```bash
export GOOGLE_CLOUD_API_KEY="your-api-key"
```

## Usage

### Running the Agent
Run the main agent script with a query:

```bash
python3 agent.py "What is the mission of stewardship in this context?"
```

### Verification & Testing
Run the verification script to test groundedness, source lockdown, and citations:

```bash
python3 verify_rag.py
```

## Development Workflow: OpenSpec

This project uses **OpenSpec**, a specification-driven development workflow. All major changes follow a formal lifecycle:

1.  **Propose**: Create a change in `openspec/changes/<name>/` with a proposal, design, and tasks.
2.  **Spec**: Define requirements in `specs/<name>/spec.md`.
3.  **Apply**: Implement the tasks defined in the change.
4.  **Archive**: Sync the delta specs to the main `openspec/specs/` directory and move the change to the archive.

For more details on the specifications, see the [openspec/specs/](./openspec/specs/) directory.
