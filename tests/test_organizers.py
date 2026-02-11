import unittest
from unittest.mock import Mock, MagicMock
from eventyay.client import EventyayClient
from eventyay.organizers import Organizers

class TestOrganizers(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=EventyayClient)
        self.organizers = Organizers(self.mock_client)

    def test_get_organizer(self):
        # Arrange
        organizer_id = "1"
        expected_response = {"id": "1", "name": "Test Organizer"}
        self.mock_client._get.return_value = expected_response

        # Act
        result = self.organizers.get_organizer(organizer_id)

        # Assert
        self.mock_client._get.assert_called_once_with("organizers/1")
        self.assertEqual(result, expected_response)

    def test_get_organizer_events(self):
        # Arrange
        organizer_id = "1"
        expected_response = [{"id": "101", "name": "Event 1"}, {"id": "102", "name": "Event 2"}]
        self.mock_client._get.return_value = expected_response

        # Act
        result = self.organizers.get_organizer_events(organizer_id)

        # Assert
        self.mock_client._get.assert_called_once_with("organizers/1/events")
        self.assertEqual(result, expected_response)

if __name__ == '__main__':
    unittest.main()
