import unittest
from unittest.mock import Mock, MagicMock
from eventyay.client import EventyayClient

class TestOrganizers(unittest.TestCase):
    def setUp(self):
        # Create a real client but mock the internal session to avoid network calls
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_get_organizer(self):
        # Arrange
        organizer_id = "1"
        expected_response = {"id": "1", "name": "Test Organizer"}
        
        # Mock the response object
        mock_response = Mock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        # Act
        result = self.client.get_organizer(organizer_id)

        # Assert
        # Verify get was called with correct URL
        self.client.session.get.assert_called_once()
        args, kwargs = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("organizers/1"))
        self.assertEqual(result, expected_response)

    def test_get_organizer_events(self):
        # Arrange
        organizer_id = "1"
        expected_response = [{"id": "101", "name": "Event 1"}, {"id": "102", "name": "Event 2"}]
        
        # Mock the response object
        mock_response = Mock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        # Act
        result = self.client.get_organizer_events(organizer_id)

        # Assert
        # Verify get was called with correct URL
        self.client.session.get.assert_called_once()
        args, kwargs = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("organizers/1/events"))
        self.assertEqual(result, expected_response)

if __name__ == '__main__':
    unittest.main()
