from google import genai
from google.genai import types
import os
import asyncio
from typing import Optional, AsyncGenerator, List, Dict
from config import get_config
import pypdf

import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stewardship-ai")

EXTENSION_GROUPS = {
    "pdf": [".pdf"],
    "word": [".doc", ".docx", ".dotx"],
    "txt": [".txt", ".md", ".csv", ".json"],
}

SYSTEM_INSTRUCTION = """You are a professional and pastoral Stewardship Guide for {diocese_name}. Your goal is to help {persona_label}s understand and live out the mission of stewardship (Time, Talent, and Treasure) using ONLY the information contained in the provided official sources.

{persona_instruction}

Use the following Source Hierarchy for all responses:
1. Universal Doctrine: Ground all moral, theological, and social principles in the Magisterium documents (e.g., Catechism, Papal encyclicals). These define the "What" and the "Why" of our mission.
2. Practical Application: Ground all specific guidance on implementation, local parish life, and practical "how-to" steps in the Stewardship resources. These define the "How" of our mission.
3. Synthesis: Always ensure practical advice is consistent with universal doctrine.

Use the following rules for all responses:

IMMEDIATE ANSWER: Start your response immediately with the information requested. FORBID the use of any greetings (e.g., "Welcome", "Dear Parishioner", "Hello", "Greetings"), raw identifiers (e.g., email addresses), or flowery preambles (e.g., "It's wonderful to talk about...", "Thank you for asking..."). Do not acknowledge the user's persona or identity in the output text.

Tone and Style: Be direct, concise, and pastoral. Avoid repetitive encouragement, pandering language, or "fluff". Focus on delivering the core facts and guidance from the sources.

Source Lockdown: Do not use any outside knowledge, general training data, or external theological facts not explicitly stated in the provided documents. Weave information from the sources naturally into your conversational response.

Pastoral Refusal: If a question asks for information not found in the sources, respond gracefully: 'I'm sorry, but our official stewardship resources don't cover that specific topic. You may want to reach out to the stewardship office for further guidance.'

Markdown Formatting: ALWAYS use structured markdown. Use double newlines (two carriage returns) between paragraphs and between each item in a list (bulleted or numbered). Use bolding (**term**) for emphasis on key stewardship concepts.
"""

PRIEST_INSTRUCTION = "Focus your guidance on leadership, parish administration, and how to cultivate a culture of stewardship within their community."
PARISHIONER_INSTRUCTION = "Focus your guidance on personal spiritual practice and practical ways to get involved in Time, Talent, and Treasure."
RESEARCHER_INSTRUCTION = "Focus your guidance on deep theological analysis, cross-document synthesis between universal doctrine and local practice, and providing academic writing support. You are specifically tasked with helping the user revise academic or complex text into approachable, pastoral language. Use modern analogies found in the RAG sources to simplify complex concepts. You MUST provide clear citations to the source documents for every major claim or finding you present."

class GCPRagAgent:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.config = get_config()
        self.model = model

        # The GenAI SDK handles authentication prioritization:
        # If project/location are provided, use Vertex AI mode (ADC).
        # Otherwise, fall back to API Key if available.
        if self.config.project_id and self.config.location:
            self.client = genai.Client(
                vertexai=True,
                project=self.config.project_id,
                location=self.config.location,
            )
        else:
            self.client = genai.Client(
                api_key=self.config.api_key,
            )

    async def _manual_retrieve(self, prompt: str, corpus_id: str, allowed_extensions: List[str]) -> List[str]:
        """Manually fetches chunks via REST API to bypass broken metadata filters."""
        import httpx
        import google.auth
        from google.auth.transport.requests import Request as GoogleAuthRequest

        # 1. Get Authentication Token
        credentials, _ = google.auth.default()
        if not credentials.valid:
            credentials.refresh(GoogleAuthRequest())

        # 2. Build REST URL
        url = f"https://{self.config.location}-aiplatform.googleapis.com/v1beta1/projects/{self.config.project_id}/locations/{self.config.location}:retrieveContexts"
        
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": {
                "text": prompt,
                "similarityTopK": 20
            },
            "vertexRagStore": {
                "ragResources": [{"ragCorpus": corpus_id}]
            }
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
        if resp.status_code != 200:
            logger.error(f"Retrieval API failed: {resp.status_code} {resp.text}")
            return []
            
        data = resp.json()
        contexts = data.get("contexts", {}).get("contexts", [])
        
        if not allowed_extensions:
            return []
            
        # 3. Filter the chunks using Python logic
        flat_allowed = []
        for group in allowed_extensions:
            if group in EXTENSION_GROUPS:
                flat_allowed.extend(EXTENSION_GROUPS[group])
            else:
                flat_allowed.append(group.lower())
                
        filtered_texts = []
        uris_seen = []
        for ctx in contexts:
            source_uri = ctx.get("sourceUri", "").lower()
            text = ctx.get("text", "")
            if not text:
                continue
                
            is_known_type = any(source_uri.endswith(ext) for group in EXTENSION_GROUPS.values() for ext in group)
            
            matches_filter = False
            if "other" in allowed_extensions and not is_known_type:
                matches_filter = True
            else:
                matches_filter = any(source_uri.endswith(ext) for ext in flat_allowed)
                
            if matches_filter:
                filtered_texts.append(text)
                uris_seen.append(ctx.get("sourceUri", "unknown"))
                
        if filtered_texts:
            logger.info(f"RAG | Filtered {len(filtered_texts)} chunks from corpus {corpus_id}. Source URIs: {list(set(uris_seen))}")
                
        return filtered_texts

    async def _get_generate_content_config(self, user_email: str, persona: str = "parishioner", system_instruction_extra: str = "") -> types.GenerateContentConfig:
        if persona == "priest":
            persona_instruction = PRIEST_INSTRUCTION
            persona_label = "Priest"
        elif persona == "researcher":
            persona_instruction = RESEARCHER_INSTRUCTION
            persona_label = "Academic / Researcher"
        else:
            persona_instruction = PARISHIONER_INSTRUCTION
            persona_label = "Parishioner"
        
        system_instruction_text = SYSTEM_INSTRUCTION.format(
            diocese_name=self.config.diocese_name,
            persona_label=persona_label,
            persona_instruction=persona_instruction
        )

        if system_instruction_extra:
            system_instruction_text += "\n\n" + system_instruction_extra

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
            system_instruction=[types.Part.from_text(text=system_instruction_text)],
        )

    async def generate_response(self, prompt: str, user_email: str, persona: str = "parishioner", history: Optional[List[dict]] = None, corpus_ids: Optional[List[str]] = None, extension_filters: Optional[Dict[str, List[str]]] = None, file_uri: Optional[str] = None, mime_type: Optional[str] = None):
        """Generates a response using synthetic RAG via REST API manual retrieval."""
        logger.info(f"AUDIT | {datetime.now().isoformat()} | User: {user_email} | Persona: {persona} | Prompt: {prompt} | File: {file_uri} | Mime: {mime_type} | Corpora: {corpus_ids} | Filters: {extension_filters}")
        
        active_corpus_ids = corpus_ids if corpus_ids is not None else [self.config.rag_corpus_id]
        
        # 1. Retrieval Phase via REST API
        all_filtered_texts = []
        for c_id in active_corpus_ids:
            try:
                allowed = (extension_filters or {}).get(c_id, ["pdf", "word", "txt", "other"])
                filtered = await self._manual_retrieve(prompt, c_id, allowed)
                all_filtered_texts.extend(filtered)
            except Exception as e:
                logger.error(f"Manual retrieval failed for corpus {c_id}: {e}")

        # 2. Context Construction
        synthetic_context = ""
        if all_filtered_texts:
            synthetic_context = "OFFICIAL SOURCE CONTEXT:\n\n" + "\n\n---\n\n".join(all_filtered_texts)
        
        # 3. Prompt Preparation
        contents = []
        
        # Prepend extracted text from uploaded file if present
        if file_uri and os.path.exists(file_uri):
            try:
                extracted_text = ""
                actual_mime_type = mime_type or "application/pdf"
                if actual_mime_type == "application/pdf":
                    reader = pypdf.PdfReader(file_uri)
                    for page in reader.pages:
                        extracted_text += (page.extract_text() or "") + "\n"
                else:
                    with open(file_uri, "r", encoding="utf-8", errors="ignore") as f:
                        extracted_text = f.read()
                
                if extracted_text.strip():
                    contents.append(
                        types.Content(
                            role="user",
                            parts=[types.Part.from_text(text=f"SESSION DOCUMENT CONTENT:\n\n{extracted_text}")]
                        )
                    )
            except Exception as e:
                logger.error(f"Failed to extract text from {file_uri}: {e}")

        # Add synthetic context if any
        if synthetic_context:
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=synthetic_context)]
                )
            )

        if history:
            for msg in history:
                role = "model" if msg["role"] == "assistant" else "user"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))
        
        # Add current prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        )
        
        # 4. Generation Phase
        system_instruction_extra = ""
        if not all_filtered_texts and not (file_uri and os.path.exists(file_uri)):
            # Pastoral refusal if no context found after filtering
            system_instruction_extra = "IMPORTANT: No relevant official documents were found matching the user's requested type. Inform the user gracefully that our official resources don't cover this topic in the requested format."

        config = await self._get_generate_content_config(
            user_email=user_email,
            persona=persona,
            system_instruction_extra=system_instruction_extra
        )

        return await self.client.aio.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config,
        )
