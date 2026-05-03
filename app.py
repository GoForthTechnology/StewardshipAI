import streamlit as st
from rag_agent import GCPRagAgent
import os
from typing import List
import firebase_admin
from firebase_admin import auth, credentials
from config import get_config

# --- Configuration & Auth ---
config = get_config()

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    # Firebase ID tokens use the Project ID (slug) for the 'aud' claim.
    # If the user provided a Project Number, we try to extract the slug from the auth domain.
    fb_project_id = config.project_id
    if fb_project_id.isdigit() and config.firebase_auth_domain:
        fb_project_id = config.firebase_auth_domain.split('.')[0]
    
    firebase_admin.initialize_app(options={
        'projectId': fb_project_id
    })

def verify_token(id_token: str):
    """Verifies the Firebase ID Token and returns user info."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        st.error(f"Authentication Failed: {e}")
        return None

# Page configuration
st.set_page_config(page_title="StewardshipAI Research Assistant", page_icon="🤖")

# --- UI Customization ---
# Hide the Streamlit "Deploy" button and header menu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Authentication UI ---
if "user_email" not in st.session_state:
    st.title("🔐 Authentication Required")
    st.info("Please sign in with your Google account to access the research agent.")
    
    # Custom component for Firebase Google SSO
    from fb_streamlit_auth import fb_streamlit_auth
    
    auth_result = fb_streamlit_auth(
        config.firebase_api_key or "",
        config.firebase_auth_domain or "",
        config.project_id or "",
        config.firebase_database_url or "",
        config.firebase_storage_bucket or "",
        config.firebase_messaging_sender_id or "",
        config.firebase_app_id or "",
        config.firebase_measurement_id or ""
    )
    
    if auth_result:
        # Debug: Print keys to terminal to help diagnose if token is missing
        # print(f"DEBUG: auth_result keys: {list(auth_result.keys())}")
        
        # The token is often nested in stsTokenManager for this component
        id_token = auth_result.get("idToken")
        if not id_token:
            # Try common fallback locations in the serialized Firebase user object
            sts = auth_result.get("stsTokenManager")
            if isinstance(sts, dict):
                id_token = sts.get("accessToken")
            if not id_token:
                id_token = auth_result.get("accessToken")

        if id_token:
            user_info = verify_token(id_token)
            
            if user_info:
                st.session_state.user_email = user_info.get("email")
                st.rerun()
        else:
            st.error("Authentication Error: Token not found in login response. Please check terminal logs.")
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
            response_stream = st.session_state.agent.generate_response(prompt, st.session_state.user_email)
            
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
