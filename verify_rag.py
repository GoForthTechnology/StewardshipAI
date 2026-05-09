from rag_agent import GCPRagAgent

def test_agent(prompt, label, persona="parishioner", user_email="test@example.com"):
    try:
        agent = GCPRagAgent()
    except Exception as e:
        print(f"Failed to initialize agent for test '{label}': {e}")
        return
    
    print(f"--- Test Case: {label} (Persona: {persona}) ---")
    print(f"Prompt: {prompt}")
    print("Response: ", end="")
    
    try:
        response_stream = agent.generate_response(prompt, user_email=user_email, persona=persona)
        full_response = ""
        for chunk in response_stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                text = chunk.text
                print(text, end="", flush=True)
                full_response += text
        print("\n")
        return full_response
    except Exception as e:
        print(f"\nError: {e}\n")
        return str(e)

if __name__ == "__main__":
    print("Verifying RAG Agent with environment-driven configuration...\n")
    
    # Test 1: Grounded answer
    test_agent("What is the primary objective of this project according to the documents?", "Grounded Answer")
    
    # Test 2: Outside scope (Pastoral Refusal Check)
    test_agent("What is the weather in Tokyo today?", "Pastoral Refusal")
    
    # Test 3: Knowledge check
    test_agent("List three specific facts from the documents about stewardship in the diocese.", "Knowledge Check")

    # Test 4: Persona Shift (Priest)
    test_agent("How can I inspire my parish for stewardship?", "Persona: Priest", persona="priest")

    # Test 5: Persona Shift (Parishioner)
    test_agent("How can I get more involved in time and talent?", "Persona: Parishioner", persona="parishioner")

    # Test 6: Persona Shift (Academic / Researcher)
    test_agent("Synthesize the main theological themes regarding stewardship.", "Persona: Researcher", persona="researcher")
