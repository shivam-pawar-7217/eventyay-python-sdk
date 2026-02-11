import unittest
from unittest.mock import MagicMock
from eventyay import EventyayClient

class TestEvents(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.mock_response = MagicMock()
        self.client.session.get = MagicMock(return_value=self.mock_response)

    def test_get_events_success(self):
        # Setup mock
        expected_data = {'data': [{'id': 1, 'name': 'Test Event'}]}
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = expected_data

        # Call method
        result = self.client.get_events(page=1, page_size=10)

        # detailed assertions
        self.client.session.get.assert_called_with(
            'https://dev.eventyay.com/api/v1/events/',
            params={'page': 1, 'page_size': 10}
        )
        self.assertEqual(result, expected_data)

if __name__ == '__main__':
    unittest.main()
