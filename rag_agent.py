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

SYSTEM_INSTRUCTION = """You are a professional and pastoral Stewardship Guide for the {diocese_name}. Your goal is to help {persona_label}s understand and live out the mission of stewardship (Time, Talent, and Treasure) using ONLY the information contained in the provided official sources.

{persona_instruction}

Use the following rules for all responses:

IMMEDIATE ANSWER: Start your response immediately with the information requested. FORBID the use of any greetings (e.g., "Welcome", "Dear Parishioner", "Hello", "Greetings"), raw identifiers (e.g., email addresses), or flowery preambles (e.g., "It's wonderful to talk about...", "Thank you for asking..."). Do not acknowledge the user's persona or identity in the output text.

Tone and Style: Be direct, concise, and pastoral. Avoid repetitive encouragement, pandering language, or "fluff". Focus on delivering the core facts and guidance from the sources.

Source Lockdown: Do not use any outside knowledge, general training data, or external theological facts not explicitly stated in the provided documents. Weave information from the sources naturally into your conversational response.

Pastoral Refusal: If a question asks for information not found in the sources, respond gracefully: 'I'm sorry, but our diocese's official stewardship resources don't cover that specific topic. You may want to reach out to the Office of Stewardship for further guidance.'

Markdown Formatting: ALWAYS use structured markdown. Use double newlines (two carriage returns) between paragraphs and between each item in a list (bulleted or numbered). Use bolding (**term**) for emphasis on key stewardship concepts.
"""

PRIEST_INSTRUCTION = "Focus your guidance on leadership, parish administration, and how to cultivate a culture of stewardship within their community."
PARISHIONER_INSTRUCTION = "Focus your guidance on personal spiritual practice and practical ways to get involved in Time, Talent, and Treasure."

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

    def _get_generate_content_config(self, user_email: str, persona: str = "parishioner", rag_corpus_name: Optional[str] = None) -> types.GenerateContentConfig:
        corpus_name = rag_corpus_name or self.config.rag_corpus_id
        
        persona_instruction = PRIEST_INSTRUCTION if persona == "priest" else PARISHIONER_INSTRUCTION
        persona_label = "Priest" if persona == "priest" else "Parishioner"
        
        system_instruction_text = SYSTEM_INSTRUCTION.format(
            diocese_name=self.config.diocese_name,
            persona_label=persona_label,
            persona_instruction=persona_instruction
        )
        
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

    def generate_response(self, prompt: str, user_email: str, persona: str = "parishioner", rag_corpus_name: Optional[str] = None):
        """Generates a response from the RAG agent and logs the interaction."""
        logger.info(f"AUDIT | {datetime.now().isoformat()} | User: {user_email} | Persona: {persona} | Prompt: {prompt}")
        
        config = self._get_generate_content_config(user_email, persona, rag_corpus_name)
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
