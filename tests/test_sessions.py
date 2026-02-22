import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Session

class TestSessionsAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_session_data = {
            "id": 101,
            "title": "Introduction to Python",
            "description": "Learn the basics of Python programming.",
            "starts_at": "2026-02-22T10:00:00Z",
            "ends_at": "2026-02-22T11:00:00Z"
        }
    
    @patch('eventyay.client.requests.Session.get')
    def test_get_session(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_session_data
        mock_get.return_value = mock_response

        # Call the method
        session = self.client.get_session("test-event", "101")

        # Assertions
        self.assertIsInstance(session, Session)
        self.assertEqual(session.id, 101)
        self.assertEqual(session.title, "Introduction to Python")
        self.assertEqual(session.starts_at, "2026-02-22T10:00:00Z")

        # Verify the correct URL was called
        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/sessions/101", 
            params=None
        )

if __name__ == '__main__':
    unittest.main()
