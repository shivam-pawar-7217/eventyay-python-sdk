import unittest
from unittest.mock import MagicMock, patch
from eventyay.client import EventyayClient


class TestPagination(unittest.TestCase):

    @patch("eventyay.client.EventyayClient._get")
    def test_get_all_organizers_pagination(self, mock_get):
        # Setup mock to return 2 pages of data
        mock_get.side_effect = [
            # Page 1 response
            {
                "data": [{"id": 1, "name": "Org 1"}],
                "links": {"next": "https://api.eventyay.com/v1/organizers?page=2"},
            },
            # Page 2 response
            {
                "data": [{"id": 2, "name": "Org 2"}],
                "links": {"next": None},  # No more pages
            },
        ]

        client = EventyayClient()
        # limit page_size to ensure we trigger pagination logic if used
        all_orgs = client.get_all_organizers()

        self.assertEqual(len(all_orgs), 2)
        self.assertEqual(all_orgs[0].name, "Org 1")
        self.assertEqual(all_orgs[1].name, "Org 2")
        self.assertEqual(mock_get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
