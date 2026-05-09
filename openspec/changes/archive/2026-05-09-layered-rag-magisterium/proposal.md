# Proposal: Layered RAG Magisterium

## Goal
Ground the Stewardship AI agent in the universal teachings of the Catholic Church (Magisterium) while maintaining the practical, parish-level guidance currently provided.

## Problem
Currently, the agent is restricted to one priest's writings. While comprehensive for practical stewardship, it lacks the broader theological guardrails provided by foundational Church documents like the Catechism, Papal encyclicals (e.g., on AI, environment), and the Compendium of Catholic Social Doctrine. This limits its ability to answer complex moral or systemic questions with authoritative grounding.

## Proposed Solution
Implement a "Layered RAG" approach using two distinct Vertex AI RAG Corpora:

1.  **Stewardship Corpus**: Existing corpus containing local, practical stewardship resources.
2.  **Magisterium Corpus**: New corpus containing universal Church documents (Catechism, Social Doctrine, Papal publications).

The agent will be configured to query both corpora simultaneously. The system instructions will be updated to guide the agent on how to synthesize these two layers (Principles vs. Practice).

## Scope
- **Configuration**: Add `GCP_MAGISTERIUM_CORPUS_ID` to environment variables and Pydantic config.
- **Agent Logic**: Update `GCPRagAgent` to include both corpora in the `VertexRagStore` tools.
- **Instruction Engineering**: Refine `SYSTEM_INSTRUCTION` to prioritize moral/theological principles from the Magisterium while keeping parish guidance focused on execution.
- **Verification**: Update `verify_rag.py` to include checks for Magisterium-level questions (e.g., "What is the Church's view on AI and human dignity?").

## Risks
- **Retrieval Noise**: Querying two corpora might dilute results if search parameters aren't tuned.
- **Token Usage**: Multiple retrieval contexts will increase input tokens.
- **Consistency**: Potential for conflicting guidance if documents aren't properly prioritized in the system prompt.
