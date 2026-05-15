import asyncio
import json
import logging
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
from rag_agent import GCPRagAgent
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

class TestObservabilityMock(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Setup in-memory span exporter for verification
        self.exporter = InMemorySpanExporter()
        self.provider = TracerProvider()
        self.provider.add_span_processor(SimpleSpanProcessor(self.exporter))
        trace.set_tracer_provider(self.provider)
        self.tracer = trace.get_tracer("stewardship-ai")

    async def test_parallel_retrieval_and_spans(self):
        # Mock dependencies in GCPRagAgent
        with patch('google.genai.Client'), \
             patch('google.auth.default', return_value=(MagicMock(), 'project-id')), \
             patch('httpx.AsyncClient.post') as mock_post:

            # Mock successful retrieval response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "contexts": {
                    "contexts": [
                        {"text": "mock text 1", "sourceUri": "file1.pdf"},
                        {"text": "mock text 2", "sourceUri": "file2.txt"}
                    ]
                }
            }
            mock_post.return_value = mock_response

            # Initialize agent
            agent = GCPRagAgent()
            
            # Setup mock stream for generate_content_stream
            mock_stream = AsyncMock()
            async def mock_iter():
                yield MagicMock(text="final answer")
            mock_stream.__aiter__.return_value = mock_iter()
            agent.client.aio.models.generate_content_stream = AsyncMock(return_value=mock_stream)

            # Trigger response with multiple corpora to test parallelization
            prompt = "What is stewardship?"
            user_email = "test@example.com"
            corpus_ids = ["corpus-1", "corpus-2"]
            
            await agent.generate_response(
                prompt=prompt,
                user_email=user_email,
                corpus_ids=corpus_ids
            )

            # 1. Verify parallelization: httpx.post should be called twice (one for each corpus)
            self.assertEqual(mock_post.call_count, 2)

            # 2. Verify spans were created
            spans = self.exporter.get_finished_spans()
            span_names = [s.name for s in spans]
            
            self.assertIn("agent_generate_response", span_names)
            self.assertIn("retrieval_phase", span_names)
            self.assertIn("rag_manual_retrieve", span_names)
            self.assertIn("context_construction_phase", span_names)
            self.assertIn("generation_phase", span_names)

            # 3. Verify attributes
            gen_span = next(s for s in spans if s.name == "agent_generate_response")
            self.assertEqual(gen_span.attributes["total_chunks_retrieved"], 4) # 2 chunks * 2 corpora

            retrieve_spans = [s for s in spans if s.name == "rag_manual_retrieve"]
            self.assertEqual(len(retrieve_spans), 2)
            self.assertIn(retrieve_spans[0].attributes["corpus_id"], corpus_ids)
            self.assertEqual(retrieve_spans[0].attributes["chunks_count"], 2)

if __name__ == "__main__":
    unittest.main()
