# Synthetic RAG Filtering Specification

## Purpose
Define the behavior for manual RAG retrieval and Python-side metadata filtering to overcome native infrastructure limitations.

## Requirements

### Requirement: Explicit REST-Based RAG Retrieval
The agent SHALL perform an explicit retrieval step using the Vertex AI `retrieveContexts` REST API to obtain raw text chunks and their source metadata. 

*Rationale: Native Managed RAG CEL filters (`contains`, `endsWith`) were found to be unsupported (501 Unimplemented) in the target region/version.*

#### Scenario: Retrieving chunks via REST
- **WHEN** a query is received
- **THEN** the agent SHALL fetch the top 20 chunks for each selected corpus using a manual `httpx` POST request.

### Requirement: Python-Side Extension Filtering
The agent SHALL filter the retrieved text chunks in Python based on the file extension of their source URI.

#### Scenario: Filtering for Word only
- **WHEN** the user has selected "Word" as the only allowed extension
- **THEN** the agent SHALL discard all retrieved chunks whose `source_uri` does not end in a Word-related extension (e.g., .doc, .docx).

### Requirement: Synthetic Context Augmentation
The agent SHALL inject the filtered chunks as a "Synthetic RAG" context into the system prompt.

#### Scenario: Answering with synthetic context
- **WHEN** filtering is complete
- **THEN** the agent SHALL prepend the text of the remaining chunks to the message history.
- **AND** the agent SHALL call `generate_content_stream` without the managed retrieval tool.

### Requirement: Empty Result Handling
The agent SHALL gracefully handle cases where all retrieved results are filtered out.

#### Scenario: No results after filtering
- **WHEN** all chunks retrieved from the RAG engine are excluded by the extension filters
- **THEN** the agent SHALL respond with a pastoral message stating that no relevant documents of the requested type were found.
