import asyncio
import os
import json
from rag_agent import GCPRagAgent
from config import get_config

async def verify():
    config = get_config()
    agent = GCPRagAgent()
    
    prompt = "stewardship" # Generic prompt to get hits
    corpus_id = config.rag_corpus_id
    
    # Test cases: [Filter Name, Allowed List]
    test_cases = [
        ["All (Default)", ["pdf", "word", "txt", "other"]],
        ["PDF Only", ["pdf"]],
        ["Word Only", ["word"]],
        ["TXT/MD Only", ["txt"]],
    ]
    
    print(f"--- Verifying RAG Filtering for Corpus: {corpus_id} ---\n")
    
    for label, filters in test_cases:
        print(f"Testing Filter: {label} ({filters})")
        try:
            # We call the internal method directly to see the raw filtered URIs
            # To do this easily, we'll temporarily modify _manual_retrieve to return URIs too,
            # or just replicate the logic here.
            
            # Replicating logic for verification transparency
            import httpx
            import google.auth
            from google.auth.transport.requests import Request as GoogleAuthRequest
            from rag_agent import EXTENSION_GROUPS

            credentials, _ = google.auth.default()
            if not credentials.valid:
                credentials.refresh(GoogleAuthRequest())

            url = f"https://{config.location}-aiplatform.googleapis.com/v1beta1/projects/{config.project_id}/locations/{config.location}:retrieveContexts"
            headers = {"Authorization": f"Bearer {credentials.token}", "Content-Type": "application/json"}
            payload = {"query": {"text": prompt, "similarityTopK": 10}, "vertexRagStore": {"ragResources": [{"ragCorpus": corpus_id}]}}
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
            if resp.status_code != 200:
                print(f"  Error: API failed with {resp.status_code}")
                continue
                
            data = resp.json()
            contexts = data.get("contexts", {}).get("contexts", [])
            
            flat_allowed = []
            for group in filters:
                if group in EXTENSION_GROUPS:
                    flat_allowed.extend(EXTENSION_GROUPS[group])
                else:
                    flat_allowed.append(group.lower())
            
            matches = []
            for ctx in contexts:
                uri = ctx.get("sourceUri", "")
                is_known_type = any(uri.lower().endswith(ext) for group in EXTENSION_GROUPS.values() for ext in group)
                
                matches_filter = False
                if "other" in filters and not is_known_type:
                    matches_filter = True
                else:
                    matches_filter = any(uri.lower().endswith(ext) for ext in flat_allowed)
                
                if matches_filter:
                    matches.append(uri)
            
            if not matches:
                print("  Result: [No matching files found for this filter]")
            else:
                for m in matches:
                    print(f"  Result: MATCHED -> {m}")
        except Exception as e:
            print(f"  Error: {e}")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(verify())
