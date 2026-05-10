from fastapi import FastAPI, Depends, HTTPException, Security, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import auth
from config import get_config
from rag_agent import GCPRagAgent
from pydantic import BaseModel
from typing import Optional, List
import logging
import json
import os
import asyncio

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
    history: Optional[List[dict]] = None
    file_uri: Optional[str] = None
    mime_type: Optional[str] = None

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

async def stream_agent_response(prompt: str, user_email: str, persona: str, history: Optional[List[dict]] = None, file_uri: Optional[str] = None, mime_type: Optional[str] = None):
    """Generator to stream agent response chunks as JSON."""
    try:
        async with asyncio.timeout(60):
            response_stream = await agent.generate_response(
                prompt=prompt,
                user_email=user_email,
                persona=persona,
                history=history,
                file_uri=file_uri,
                mime_type=mime_type
            )
            async for chunk in response_stream:
                if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                    text = chunk.text
                    yield f"data: {json.dumps({'text': text})}\n\n"
    except asyncio.TimeoutError:
        logger.error(f"Generation timed out for user: {user_email}")
        yield f"data: {json.dumps({'error': 'The request took too long to process. Please try again.'})}\n\n"
    except Exception as e:
        logger.error(f"Error in stream_agent_response: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.post("/chat")
async def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    user_email = user.get("email", "unknown")
    return StreamingResponse(
        stream_agent_response(
            prompt=request.prompt,
            user_email=user_email,
            persona=request.persona,
            history=request.history,
            file_uri=request.file_uri,
            mime_type=request.mime_type
        ),
        media_type="text/event-stream"
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    """Handles file uploads for session-persistent context."""
    # 1.1 Validation: Size (10MB)
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
    
    # 1.1 Validation: Type (PDF/Text)
    ALLOWED_TYPES = ["application/pdf", "text/plain"]
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF or Text document.")
    
    # 1.2 Local storage for Vertex AI compatibility
    UPLOAD_DIR = "/tmp/stewardship-uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    try:
        # Use a unique ID to prevent collisions
        import uuid
        file_id = str(uuid.uuid4())
        file_extension = "pdf" if file.content_type == "application/pdf" else "txt"
        safe_filename = f"{file_id}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {
            "file_uri": file_path, # We pass the local path as the 'uri'
            "display_name": file.filename,
            "mime_type": file.content_type
        }
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
