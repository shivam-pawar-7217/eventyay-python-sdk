import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Microlocation, MicrolocationList


class TestMicrolocationsAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_microlocation_data = {
            "id": 1,
            "name": "Main Hall",
            "latitude": 52.5200,
            "longitude": 13.4050,
            "floor": 1,
            "room": "A101"
        }

    @patch('eventyay.client.requests.Session.get')
    def test_get_event_microlocations(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                self.mock_microlocation_data,
                {
                    "id": 2,
                    "name": "Workshop Room B",
                    "floor": 2,
                    "room": "B201"
                }
            ],
            "meta": {"total": 2}
        }
        mock_get.return_value = mock_response

        result = self.client.get_event_microlocations(
            "test-event", page=1, page_size=10
        )

        self.assertIsInstance(result, MicrolocationList)
        self.assertEqual(len(result.data), 2)

        first = result.data[0]
        self.assertIsInstance(first, Microlocation)
        self.assertEqual(first.id, 1)
        self.assertEqual(first.name, "Main Hall")
        self.assertEqual(first.floor, 1)

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/"
            "events/test-event/microlocations",
            params={'page': 1, 'page_size': 10}
        )

    @patch('eventyay.client.requests.Session.get')
    def test_get_microlocation(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_microlocation_data
        mock_get.return_value = mock_response

        result = self.client.get_microlocation("test-event", "1")

        self.assertIsInstance(result, Microlocation)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Main Hall")
        self.assertEqual(result.room, "A101")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/"
            "events/test-event/microlocations/1",
            params=None
        )


if __name__ == '__main__':
    unittest.main()
