from google import genai
from google.genai import types
import os
from typing import Optional, AsyncGenerator
from config import get_config

import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stewardship-ai")

SYSTEM_INSTRUCTION = """You are a strict research assistant. Your goal is to answer questions using ONLY the information contained in the provided sources. Use the following rules for all responses:

Source Lockdown: Do not use any outside knowledge, general training data, or external facts not explicitly stated in the uploaded documents.

Verification: If a question asks for information not found in the sources, state clearly: 'I cannot answer this because the provided sources do not contain this information.' Do not attempt to fill in gaps with outside logic.

Citations: Every claim you make must be followed by a citation to the specific source(s) used.

No Hallucination: If the sources are ambiguous, reflect that ambiguity rather than interpreting based on external context.

User Identity: You are currently assisting user: {user_email}. All responses are logged for stewardship auditing."""

class GCPRagAgent:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.config = get_config()
        self.model = model

        # The GenAI SDK handles authentication prioritization:
        # If api_key is provided, it's used.
        # Otherwise, it falls back to Application Default Credentials (ADC).
        self.client = genai.Client(
            vertexai=True,
            project=self.config.project_id,
            location=self.config.location,
            api_key=self.config.api_key,
        )

    def _get_generate_content_config(self, user_email: str, rag_corpus_name: Optional[str] = None) -> types.GenerateContentConfig:
        corpus_name = rag_corpus_name or self.config.rag_corpus_id
        
        system_instruction_text = SYSTEM_INSTRUCTION.format(user_email=user_email)
        
        tools = [
            types.Tool(
                retrieval=types.Retrieval(
                    vertex_rag_store=types.VertexRagStore(
                        rag_resources=[
                            types.VertexRagStoreRagResource(
                                rag_corpus=corpus_name
                            )
                        ],
                    )
                )
            )
        ]

        return types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=65535,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
            ],
            tools=tools,
            system_instruction=[types.Part.from_text(text=system_instruction_text)],
        )

    def generate_response(self, prompt: str, user_email: str, rag_corpus_name: Optional[str] = None):
        """Generates a response from the RAG agent and logs the interaction."""
        logger.info(f"AUDIT | {datetime.now().isoformat()} | User: {user_email} | Prompt: {prompt}")
        
        config = self._get_generate_content_config(user_email, rag_corpus_name)
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        ]
        
        return self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config,
        )
