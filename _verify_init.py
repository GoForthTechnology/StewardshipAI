import asyncio
import os
from rag_agent import GCPRagAgent

async def test():
    # Set fake env vars to bypass initialization check if possible
    os.environ["GCP_PROJECT_ID"] = "test-project"
    os.environ["GCP_RAG_CORPUS_ID"] = "test-corpus"
    
    try:
        agent = GCPRagAgent()
        print("Agent initialized")
    except Exception as e:
        print(f"Init failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
