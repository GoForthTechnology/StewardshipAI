import asyncio
from rag_agent import GCPRagAgent

async def test_agent(prompt, label, persona="parishioner", user_email="test@example.com"):
    try:
        agent = GCPRagAgent()
    except Exception as e:
        print(f"Failed to initialize agent for test '{label}': {e}")
        return
    
    print(f"--- Test Case: {label} (Persona: {persona}) ---")
    print(f"Prompt: {prompt}")
    print("Response: ", end="")
    
    try:
        response_stream = await agent.generate_response(prompt, user_email=user_email, persona=persona)
        full_response = ""
        async for chunk in response_stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                text = chunk.text
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
