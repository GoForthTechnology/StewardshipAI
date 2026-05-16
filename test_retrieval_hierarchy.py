import unittest
import os
import json
from unittest.mock import MagicMock, AsyncMock, patch
from rag_agent import GCPRagAgent
from test_utils import _AsyncIterator

# Set dummy env vars
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("GCP_PROJECT_ID", "test-project")
os.environ.setdefault("GCP_RAG_CORPUS_ID", "stewardship-corpus")
os.environ.setdefault("GCP_LOCATION", "us-south1")

class TestRetrievalHierarchy(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.obs_patcher = patch('observability.setup_observability')
        self.obs_patcher.start()
        
        # Patch the global tracer provider and the get_tracer helper
        self.tp_patcher = patch('opentelemetry.trace.get_tracer_provider')
        self.tp_patcher.start()
        self.tracer_patcher = patch('rag_agent.get_tracer')
        self.tracer_patcher.start()

        # Patch auth globally for these tests
        self.global_auth_patcher = patch('google.auth.default', return_value=(MagicMock(), 'test-project'))
        self.global_auth_patcher.start()

    def tearDown(self):
        self.global_auth_patcher.stop()
        self.tracer_patcher.stop()
        self.tp_patcher.stop()
        self.obs_patcher.stop()

    async def test_Scenario_Querying_with_Selected_Corpora(self):
        """
        Scenario: Querying with Selected Corpora
        - WHEN a user submits a query to the agent with specific corpora selected
        - THEN the system SHALL verify that the retrieval tool is called with exactly those corpus IDs.
        """
        with patch('google.genai.Client'), \
             patch('httpx.AsyncClient.post') as mock_post:

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"contexts": {"contexts": [{"text": "t", "sourceUri": "d.pdf"}]}}
            mock_post.return_value = mock_response

            agent = GCPRagAgent()
            agent.client.aio.models.generate_content_stream = AsyncMock(return_value=_AsyncIterator([MagicMock(text="ans")]))

            corpus_ids = ["magisterium-id", "stewardship-id"]
            async for _ in agent.generate_response("query", "u@e.com", corpus_ids=corpus_ids):
                pass

            # Verify both corpora were queried
            self.assertEqual(mock_post.call_count, 2)
            calls = [c.kwargs['json']['vertexRagStore']['ragResources'][0]['ragCorpus'] for c in mock_post.call_args_list]
            self.assertIn("magisterium-id", calls)
            self.assertIn("stewardship-id", calls)

    async def test_Scenario_Synthesis_of_Universal_Doctrine(self):
        """
        Scenario: Synthesis of Universal Doctrine
        - WHEN a user asks a question with moral or theological implications
        - THEN the agent SHALL ground its primary response in documents from the Magisterium Corpus.
        """
        with patch('google.genai.Client'), \
             patch('httpx.AsyncClient.post') as mock_post:

            # Mock competing sources
            mock_response = MagicMock(); mock_response.status_code = 200
            mock_response.json.return_value = {
                "contexts": {
                    "contexts": [
                        {"text": "TRUTH: AI is a tool for the common good.", "sourceUri": "magisterium.pdf"},
                        {"text": "LOCAL: Our parish uses AI for scheduling.", "sourceUri": "parish.pdf"}
                    ]
                }
            }
            mock_post.return_value = mock_response

            agent = GCPRagAgent()
            # Capture the context sent to the LLM
            agent.client.aio.models.generate_content_stream = AsyncMock(return_value=_AsyncIterator([MagicMock(text="ans")]))

            corpus_ids = ["magisterium-id", "stewardship-id"]
            async for _ in agent.generate_response("Is AI ethical?", "u@e.com", corpus_ids=corpus_ids):
                pass

            call_args = agent.client.aio.models.generate_content_stream.call_args
            contents = call_args.kwargs['contents']
            context_text = contents[0].parts[0].text
            
            # Verify labeling
            self.assertIn("[SOURCE: Magisterium Corpus]", context_text)
            self.assertIn("[SOURCE: Stewardship Corpus]", context_text)
            self.assertIn("TRUTH: AI is a tool", context_text)

    async def test_Scenario_Local_Application_of_Doctrine(self):
        """
        Scenario: Local Application of Doctrine
        - WHEN a user asks for practical stewardship advice
        - THEN the agent SHALL ground its primary response in documents from the Stewardship Corpus.
        """
        with patch('google.genai.Client'), \
             patch('httpx.AsyncClient.post') as mock_post:

            mock_response = MagicMock(); mock_response.status_code = 200
            mock_response.json.return_value = {
                "contexts": {
                    "contexts": [
                        {"text": "PRACTICAL: Use the online portal for tithing.", "sourceUri": "stewardship_guide.pdf"}
                    ]
                }
            }
            mock_post.return_value = mock_response

            agent = GCPRagAgent()
            agent.client.aio.models.generate_content_stream = AsyncMock(return_value=_AsyncIterator([MagicMock(text="ans")]))

            async for _ in agent.generate_response("How do I tithe?", "u@e.com", corpus_ids=["stewardship-id"]):
                pass

            call_args = agent.client.aio.models.generate_content_stream.call_args
            contents = call_args.kwargs['contents']
            context_text = contents[0].parts[0].text
            
            self.assertIn("[SOURCE: Stewardship Corpus]", context_text)
            self.assertIn("PRACTICAL: Use the online portal", context_text)

if __name__ == "__main__":
    unittest.main()
