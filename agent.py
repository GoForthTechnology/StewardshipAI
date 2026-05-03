from rag_agent import GCPRagAgent
import sys

def main():
    try:
        agent = GCPRagAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return
    
    prompt = "What are the key findings in the documents?"
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    
    print(f"Querying RAG Agent with prompt: {prompt}\n")
    
    try:
        response_stream = agent.generate_response(prompt, user_email="cli-user@stewardship.local")
        for chunk in response_stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                print(chunk.text, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
