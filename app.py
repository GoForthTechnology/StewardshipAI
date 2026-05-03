import streamlit as st
from rag_agent import GCPRagAgent
import os
from typing import List

# --- Configuration & Auth ---
# In a real Firebase integration, these would be retrieved via Firebase SDK/Redirect
# For this implementation, we simulate the auth state.
AUTHORIZED_EMAILS = os.environ.get("AUTHORIZED_EMAILS", "").split(",")

def is_authorized(email: str) -> bool:
    """Checks if the user email is in the allow-list."""
    return email in AUTHORIZED_EMAILS

# Page configuration
st.set_page_config(page_title="StewardshipAI Research Assistant", page_icon="🤖")

# --- Authentication UI ---
if "user_email" not in st.session_state:
    st.title("🔐 Authentication Required")
    st.info("Please sign in with your authorized Google account to access the research agent.")
    
    # Placeholder for Firebase Google Login Button
    # In practice, this would trigger the Firebase Auth flow
    email_input = st.text_input("Enter your email (Simulation for Auth Flow):")
    if st.button("Sign In"):
        if is_authorized(email_input):
            st.session_state.user_email = email_input
            st.rerun()
        else:
            st.error("Access Denied: Your email is not in the authorized allow-list.")
    st.stop()

# --- Main App Interface ---
st.title("🤖 StewardshipAI Research Assistant")
st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
if st.sidebar.button("Sign Out"):
    del st.session_state.user_email
    st.rerun()

st.markdown("---")

# Initialize RAG Agent
if "agent" not in st.session_state:
    try:
        st.session_state.agent = GCPRagAgent()
    except Exception as e:
        st.error(f"Failed to initialize RAG Agent: {e}")
        st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Generate response stream
            response_stream = st.session_state.agent.generate_response(prompt)
            
            for chunk in response_stream:
                if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                    text = chunk.text
                    full_response += text
                    message_placeholder.markdown(full_response + "▌")
                
                # Check for citations/grounding metadata
                if chunk.candidates and chunk.candidates[0].grounding_metadata:
                    metadata = chunk.candidates[0].grounding_metadata
                    if metadata.search_entry_point:
                        # Display search entry point (if applicable)
                        with st.sidebar:
                            st.info("Grounding Metadata Detected")
                            st.json(metadata.search_entry_point.rendered_content)
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
