# Tasks: Layered RAG Magisterium

## 1. Data & Manual Configuration

- [x] 1.1 (Manual) Create the new Magisterium corpus via Vertex AI console or SDK.
- [x] 1.2 (Manual) Ingest doctrinal documents (Catechism, etc.) into the new corpus.
- [x] 1.3 Add `GCP_MAGISTERIUM_CORPUS_ID` to `setup_env.sh.template`.
- [x] 1.4 Update `terraform/main.tf` to pass the new `GCP_MAGISTERIUM_CORPUS_ID` environment variable to Cloud Run.

## 2. API & Configuration Core

- [x] 2.1 Add `magisterium_corpus_id` to `GCPConfig` in `config.py`.
- [x] 2.2 Update `GCPConfig.from_env()` to read `GCP_MAGISTERIUM_CORPUS_ID`.
- [x] 2.3 Update `GCPRagAgent._get_generate_content_config` to include both corpora in `rag_resources`.

## 3. Instruction Engineering

- [x] 3.1 Update `SYSTEM_INSTRUCTION` in `rag_agent.py` with the "Source Hierarchy" (Universal Principles vs. Local Practice).
- [x] 3.2 Refine `RESEARCHER_INSTRUCTION` to prioritize deep synthesis from the Magisterium corpus.

## 4. Verification

- [x] 4.1 Update `verify_rag.py` with test cases for Social Doctrine and AI ethics.
- [x] 4.2 Run integration tests to verify successful retrieval and citation from both corpora.
