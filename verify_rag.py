from rag_agent import GCPRagAgent

def test_agent(prompt, label):
    try:
        agent = GCPRagAgent()
    except Exception as e:
        print(f"Failed to initialize agent for test '{label}': {e}")
        return
    
    print(f"--- Test Case: {label} ---")
    print(f"Prompt: {prompt}")
    print("Response: ", end="")
    
    try:
        response_stream = agent.generate_response(prompt)
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
    
    # Test 2: Outside scope
    test_agent("What is the weather in Tokyo today?", "Outside Scope")
    
    # Test 3: Citation check
    test_agent("List three specific facts from the documents and provide citations for each.", "Citation Check")
