import unittest
from unittest.mock import MagicMock, patch
from eventyay import EventyayClient
from eventyay.exceptions import EventyayAPIError

class TestOrganizers(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.mock_response = MagicMock()
        self.client.session.get = MagicMock(return_value=self.mock_response)

    def test_get_organizers_success(self):
        # Setup mock
        expected_data = {'data': [{'id': 1, 'name': 'Test Organizer'}]}
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = expected_data

        # Call method
        result = self.client.get_organizers(page=1, page_size=10)

        # detailed assertions
        self.client.session.get.assert_called_with(
            'https://dev.eventyay.com/api/v1/organizers/',
            params={'page': 1, 'page_size': 10}
        )
        self.assertEqual(result, expected_data)

    def test_get_organizer_success(self):
        # Setup mock
        organizer_id = 1
        expected_data = {'id': 1, 'name': 'Test Organizer'}
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = expected_data

        # Call method
        result = self.client.get_organizer(organizer_id)

        # detailed assertions
        self.client.session.get.assert_called_with(
            f'https://dev.eventyay.com/api/v1/organizers/{organizer_id}',
            params=None
        )
        self.assertEqual(result, expected_data)

if __name__ == '__main__':
    unittest.main()
