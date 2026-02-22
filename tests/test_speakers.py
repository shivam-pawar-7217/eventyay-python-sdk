import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Speaker

class TestSpeakersAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_speaker_data = {
            "id": 1,
            "name": "Jane Doe",
            "email": "jane@example.com",
            "photo_url": "https://example.com/photo.jpg",
            "short_biography": "Software Engineer"
        }
    
    @patch('eventyay.client.requests.Session.get')
    def test_get_speaker(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_speaker_data
        mock_get.return_value = mock_response

        # Call the method
        speaker = self.client.get_speaker("test-event", "1")

        # Assertions
        self.assertIsInstance(speaker, Speaker)
        self.assertEqual(speaker.id, 1)
        self.assertEqual(speaker.name, "Jane Doe")
        self.assertEqual(speaker.short_biography, "Software Engineer")

        # Verify the correct URL was called
        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/speakers/1", 
            params=None
        )

if __name__ == '__main__':
    unittest.main()
