import asyncio
import os
from unittest.mock import MagicMock, AsyncMock, patch
from rag_agent import GCPRagAgent

# Helper for async iteration in mocks
class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)
    def __aiter__(self):
        return self
    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration

async def test_agent(prompt, label, persona="parishioner", user_email="test@example.com"):
    # If MOCK_GCP is set, we'll patch the agent's internal client and methods
    is_mock = os.environ.get("MOCK_GCP", "false").lower() == "true"
    
    try:
        if is_mock:
            with patch('google.genai.Client'), \
                 patch('google.auth.default', return_value=(MagicMock(), 'project-id')), \
                 patch('httpx.AsyncClient.post') as mock_post:
                
                # Setup mock retrieval
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "contexts": {
                        "contexts": [{"text": f"Mock context for {label}", "sourceUri": "mock.pdf"}]
                    }
                }
                mock_post.return_value = mock_response
                
                agent = GCPRagAgent()
                
                # Mock the stream generator
                mock_chunks = [
                    {"status": "🔍 Searching official resources..."},
                    {"status": "📖 Analyzing relevant documents..."},
                    {"status": "✍️ Synthesizing response..."},
                    {"text": f"This is a mocked response for the '{label}' test case. "}
                ]
                
                # If persona is researcher, add citation
                if persona == "researcher":
                    mock_chunks.append({"text": "Refer to [1]."})
                
                agent.generate_response = MagicMock(return_value=AsyncIterator(mock_chunks))
                
                return await _run_test_logic(agent, prompt, label, persona, user_email)
        else:
            agent = GCPRagAgent()
            return await _run_test_logic(agent, prompt, label, persona, user_email)
            
    except Exception as e:
        print(f"Failed to initialize or run agent for test '{label}': {e}")
        return

async def _run_test_logic(agent, prompt, label, persona, user_email):
    print(f"--- Test Case: {label} (Persona: {persona}) ---")
    print(f"Prompt: {prompt}")
    print("Response: ", end="")
    
    try:
        response_stream = agent.generate_response(prompt, user_email=user_email, persona=persona)
        full_response = ""
        async for chunk in response_stream:
            if "status" in chunk:
                print(f"[Status: {chunk['status']}] ", flush=True)
                continue
            
            if "text" in chunk:
                text = chunk["text"]
                print(text, end="", flush=True)
                full_response += text
        print("\n")
        return full_response
    except Exception as e:
        print(f"\nError: {e}\n")
        return str(e)

async def main():
    print("Verifying RAG Agent with environment-driven configuration...\n")
    
    # Test 1: Grounded answer
    await test_agent("What is the primary objective of this project according to the documents?", "Grounded Answer")
    
    # Test 2: Outside scope (Pastoral Refusal Check)
    await test_agent("What is the weather in Tokyo today?", "Pastoral Refusal")
    
    # Test 3: Knowledge check
    await test_agent("List three specific facts from the documents about stewardship.", "Knowledge Check")

    # Test 4: Persona Shift (Priest)
    await test_agent("How can I inspire my community for stewardship?", "Persona: Priest", persona="priest")

    # Test 5: Persona Shift (Parishioner)
    await test_agent("How can I get more involved in time and talent?", "Persona: Parishioner", persona="parishioner")

    # Test 6: Magisterium Knowledge (Social Doctrine)
    await test_agent("What are the core principles of Catholic Social Doctrine regarding the dignity of work?", "Magisterium: Social Doctrine")

    # Test 7: Magisterium Knowledge (AI Ethics)
    await test_agent("What is the Church's position on the ethical use of Artificial Intelligence?", "Magisterium: AI Ethics")

    # Test 8: Persona Shift (Academic / Researcher)
    await test_agent("Synthesize the main theological themes regarding stewardship.", "Persona: Researcher", persona="researcher")

if __name__ == "__main__":
    asyncio.run(main())
