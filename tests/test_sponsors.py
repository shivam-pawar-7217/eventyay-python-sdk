import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Sponsor, SponsorList


class TestSponsorsAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_sponsor_data = {
            "id": 1,
            "name": "TechCorp Inc.",
            "description": "Leading technology company.",
            "url": "https://techcorp.example.com",
            "logo_url": "https://techcorp.example.com/logo.png",
            "level": "Gold",
            "type": "sponsor"
        }

    @patch('eventyay.client.requests.Session.get')
    def test_get_event_sponsors(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                self.mock_sponsor_data,
                {
                    "id": 2,
                    "name": "DevTools Ltd.",
                    "level": "Silver"
                }
            ],
            "meta": {"total": 2}
        }
        mock_get.return_value = mock_response

        result = self.client.get_event_sponsors(
            "test-event", page=1, page_size=10
        )

        self.assertIsInstance(result, SponsorList)
        self.assertEqual(len(result.data), 2)

        first = result.data[0]
        self.assertIsInstance(first, Sponsor)
        self.assertEqual(first.id, 1)
        self.assertEqual(first.name, "TechCorp Inc.")
        self.assertEqual(first.level, "Gold")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/"
            "events/test-event/sponsors",
            params={'page': 1, 'page_size': 10}
        )

    @patch('eventyay.client.requests.Session.get')
    def test_get_sponsor(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_sponsor_data
        mock_get.return_value = mock_response

        result = self.client.get_sponsor("test-event", "1")

        self.assertIsInstance(result, Sponsor)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "TechCorp Inc.")
        self.assertEqual(result.url, "https://techcorp.example.com")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/"
            "events/test-event/sponsors/1",
            params=None
        )


if __name__ == '__main__':
    unittest.main()
