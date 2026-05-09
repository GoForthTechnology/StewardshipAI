# Design: Layered RAG Magisterium

## Architecture Overview

The system will move from a single-corpus retrieval model to a multi-corpus retrieval model.

```ascii
      REQUEST FLOW
      ════════════════════════════════════════════

      [ User Prompt ]
             │
      ┌──────▼──────┐
      │  API Layer  │ ◀── Injects Persona & User ID
      └──────┬──────┘
             │
      ┌──────▼────────┐
      │  RAG Agent    │
      │ (Gemini 2.5)  │
      └──────┬────────┘
             │
      ┌──────▼────────┐
      │ Retrieval Tool│
      └──────┬────────┘
             │
      ┌──────┴──────────────┐
      │                     │
## Configuration & Retrieval Model

The system will use environment variables to manage the IDs for both RAG corpora. This allows for manual management via the Vertex AI SDK or Console while maintaining the layered retrieval logic in the code.

### Required Environment Variables
- `GCP_RAG_CORPUS_ID`: The existing corpus for Stewardship (practical) documents.
- `GCP_MAGISTERIUM_CORPUS_ID`: The new corpus for Magisterium (doctrinal) documents.

### Architecture Overview

The system uses a multi-corpus retrieval model.

```ascii
      REQUEST FLOW
      ════════════════════════════════════════════

      [ User Prompt ]
             │
      ┌──────▼──────┐
      │  API Layer  │ ◀── Injects Persona & User ID
      └──────┬──────┘
             │
      ┌──────▼────────┐
      │  RAG Agent    │
      │ (Gemini 2.5)  │
      └──────┬────────┘
             │
      ┌──────▼────────┐
      │ Retrieval Tool│
      └──────┬────────┘
             │
      ┌──────┴──────────────┐
      │                     │
   ┌──▼────────────┐   ┌──────▼──────────┐
   │Stewardship RAG│   │ Magisterium RAG │
   │ (Practical)   │   │  (Theological)  │
   └───────────────┘   └─────────────────┘
```

## Technical Changes

### 1. Configuration (`config.py`)
Add `magisterium_corpus_id` to the `GCPConfig` class.

```python
class GCPConfig(BaseModel):
    ...
    rag_corpus_id: str
    magisterium_corpus_id: str | None = None
```

### 2. Retrieval Tool Configuration (`rag_agent.py`)
The `VertexRagStore` tool supports a list of `rag_resources`. We will populate this list dynamically based on availability of the environment variables.

```python
tools = [
    types.Tool(
        retrieval=types.Retrieval(
            vertex_rag_store=types.VertexRagStore(
                rag_resources=[
                    types.VertexRagStoreRagResource(rag_corpus=self.config.rag_corpus_id),
                    types.VertexRagStoreRagResource(rag_corpus=self.config.magisterium_corpus_id),
                ],
            )
        )
    )
]
```

### 3. Prompt Engineering
The `SYSTEM_INSTRUCTION` will be updated to include a "Source Hierarchy" section:

- **Primary Theological Authority**: Magisterium documents.
- **Primary Practical Authority**: Stewardship documents.
- **Synthesis Rule**: Use the Magisterium to define the "What" and "Why" (Universal Truth), and the Stewardship documents to define the "How" (Local Application).

## Ingestion Strategy
This proposal assumes the `GCP_MAGISTERIUM_CORPUS_ID` points to an already provisioned and populated corpus. Ingestion of the Catechism and Papal documents will be handled via the Vertex AI Console or existing GCS-to-RAG pipelines.
