from fastapi import FastAPI, Depends, HTTPException, Security, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import auth
from config import get_config
from rag_agent import GCPRagAgent
from pydantic import BaseModel
import logging
import json
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stewardship-api")

# --- Configuration & Auth ---
config = get_config()

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    fb_project_id = config.project_id
    if fb_project_id.isdigit() and config.firebase_auth_domain:
        fb_project_id = config.firebase_auth_domain.split('.')[0]
    
    firebase_admin.initialize_app(options={
        'projectId': fb_project_id
    })

app = FastAPI(title="StewardshipAI API")
security = HTTPBearer()

# Initialize RAG Agent
agent = GCPRagAgent()

class ChatRequest(BaseModel):
    prompt: str
    persona: str = "parishioner"

def get_current_user(res: HTTPAuthorizationCredentials = Security(security)):
    """Verifies the Firebase ID Token and returns user info."""
    try:
        decoded_token = auth.verify_id_token(res.credentials)
        return decoded_token
    except Exception as e:
        logger.error(f"Authentication Failed: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {e}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/config.js")
async def get_frontend_config():
    """Serves runtime configuration as a JavaScript file."""
    config = get_config()
    js_content = f"""
    window.ENV = {{
      production: true,
      firebase: {{
        apiKey: "{config.firebase_api_key or ''}",
        authDomain: "{config.firebase_auth_domain or ''}",
        projectId: "{config.project_id or ''}",
        storageBucket: "{config.firebase_storage_bucket or ''}",
        messagingSenderId: "{config.firebase_messaging_sender_id or ''}",
        appId: "{config.firebase_app_id or ''}",
        measurementId: "{config.firebase_measurement_id or ''}"
      }},
      apiUrl: ''
    }};
    """
    return Response(content=js_content, media_type="application/javascript")

async def stream_agent_response(prompt: str, user_email: str, persona: str):
    """Generator to stream agent response chunks as JSON."""
    try:
        response_stream = agent.generate_response(prompt, user_email, persona)
        for chunk in response_stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                text = chunk.text
                yield f"data: {json.dumps({'text': text})}\n\n"
            
            if chunk.candidates and chunk.candidates[0].grounding_metadata:
                metadata = chunk.candidates[0].grounding_metadata
                if metadata.grounding_chunks:
                    chunks = []
                    for gc in metadata.grounding_chunks:
                        if gc.web:
                            chunks.append({"title": gc.web.title, "uri": gc.web.uri})
                        elif gc.retrieved_context:
                            chunks.append({"title": gc.retrieved_context.title, "uri": gc.retrieved_context.uri})
                    if chunks:
                        yield f"data: {json.dumps({'citations': chunks})}\n\n"
    except Exception as e:
        logger.error(f"Error in stream_agent_response: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.post("/chat")
async def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    user_email = user.get("email", "unknown")
    return StreamingResponse(
        stream_agent_response(request.prompt, user_email, request.persona),
        media_type="text/event-stream"
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
