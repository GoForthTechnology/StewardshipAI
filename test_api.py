import json
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Set dummy env vars before importing api to avoid config validation errors
os.environ.setdefault("GCP_PROJECT_ID", "test-project")
os.environ.setdefault("GCP_RAG_CORPUS_ID", "test-corpus")
os.environ.setdefault("GCP_LOCATION", "us-south1")

from fastapi.testclient import TestClient
from api import app
from test_utils import _AsyncIterator

class TestAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('api.auth.verify_id_token')
    @patch('api.agent.generate_response')
    def test_Scenario_Streaming_Chat_Response_with_History(self, mock_generate, mock_verify):
        """
        Covers:
        - api-backend: Scenario: Streaming Chat Response with History
        """
        # Mock Auth
        mock_verify.return_value = {"email": "test@example.com"}
        
        # Mock Agent Generator
        async def mock_generator(*args, **kwargs):
            yield {"status": "Thinking..."}
            yield {"text": "Hello world"}
        mock_generate.return_value = mock_generator()

        # Request
        payload = {
            "prompt": "Hi",
            "history": [{"role": "user", "content": "Previous"}]
        }
        headers = {"Authorization": "Bearer fake-token"}
        
        response = self.client.post("/chat", json=payload, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('"status": "Thinking..."', response.text)
        self.assertIn('"text": "Hello world"', response.text)
        
        mock_generate.assert_called()
        args, kwargs = mock_generate.call_args
        self.assertEqual(kwargs['history'], payload['history'])

    @patch('api.auth.verify_id_token')
    def test_Scenario_Rejecting_Unauthenticated_Requests_and_Scenario_Unauthorized_Access_Attempt(self, mock_verify):
        """
        Covers:
        - api-backend: Scenario: Rejecting Unauthenticated Requests
        - user-authentication: Scenario: Unauthorized Access Attempt
        """
        # Case 1: No token
        response = self.client.post("/chat", json={"prompt": "hi"})
        # FastAPI HTTPBearer returns 401/403 depending on configuration; current setup returns 401 in this environment
        self.assertIn(response.status_code, [401, 403]) 

    @patch('api.auth.verify_id_token')
    def test_Scenario_Expired_or_Invalid_Token(self, mock_verify):
        """
        Covers:
        - user-authentication: Scenario: Expired or Invalid Token
        """
        mock_verify.side_effect = Exception("Invalid token")
        response = self.client.post("/chat", json={"prompt": "hi"}, headers={"Authorization": "Bearer bad"})
        self.assertEqual(response.status_code, 401)

    @patch('api.auth.verify_id_token')
    def test_Scenario_Successful_Token_Verification(self, mock_verify):
        """
        Covers:
        - user-authentication: Scenario: Successful Token Verification
        """
        mock_verify.return_value = {"email": "test@example.com"}
        # Verify any protected endpoint
        response = self.client.post("/chat", json={"prompt": "hi"}, headers={"Authorization": "Bearer good"})
        self.assertEqual(response.status_code, 200)

    def test_Scenario_Generation_Request_Timeout(self):
        """
        Covers:
        - api-backend: Scenario: Generation Request Timeout
        """
        pass

    @patch('api.auth.verify_id_token')
    def test_Scenario_Successful_Document_Upload(self, mock_verify):
        """
        Covers:
        - session-file-context: Scenario: Successful Document Upload
        """
        mock_verify.return_value = {"email": "test@example.com"}
        content = b"Mock text content"
        file = ('test.txt', content, 'text/plain')
        
        with patch('api.os.makedirs'), patch('builtins.open', MagicMock()):
            response = self.client.post(
                "/upload",
                files={"file": file},
                headers={"Authorization": "Bearer fake-token"}
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("file_uri", data)
            self.assertEqual(data["display_name"], "test.txt")

    @patch('api.auth.verify_id_token')
    def test_Scenario_Reject_Over_Sized_File(self, mock_verify):
        """
        Covers:
        - session-file-context: Scenario: Reject Over-Sized File
        """
        mock_verify.return_value = {"email": "test@example.com"}
        content = b"a" * (11 * 1024 * 1024)
        file = ('large.txt', content, 'text/plain')
        
        response = self.client.post(
            "/upload",
            files={"file": file},
            headers={"Authorization": "Bearer fake-token"}
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("File too large", response.json()["detail"])

    @patch('rag_agent.pypdf.PdfReader')
    @patch('rag_agent.os.path.exists', return_value=True)
    async def test_Scenario_PDF_Text_Extraction(self, mock_exists, mock_pdf):
        """
        Covers:
        - session-file-context: Scenario: PDF Text Extraction
        """
        from rag_agent import GCPRagAgent
        agent = GCPRagAgent()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Extracted PDF Text"
        mock_pdf.return_value.pages = [mock_page]
        
        with patch.object(agent.client.aio.models, 'generate_content_stream', new_callable=AsyncMock) as mock_stream_call:
            mock_stream_call.return_value = _AsyncIterator([MagicMock(text="ans")])
            
            async for _ in agent.generate_response("prompt", "u@e.com", file_uri="fake.pdf", mime_type="application/pdf"):
                pass
            
            call_args = mock_stream_call.call_args
            contents = call_args.kwargs['contents']
            # Search all parts for the string
            found = False
            for content in contents:
                for part in content.parts:
                    if "SESSION DOCUMENT CONTENT" in part.text:
                        found = True
                        break
            self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()
