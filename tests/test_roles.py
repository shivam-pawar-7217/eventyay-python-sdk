import unittest
from unittest.mock import Mock
from eventyay.client import EventyayClient


class TestRoles(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_get_event_roles(self):
        event_id = "1"
        expected = {
            "data": [
                {"id": 1, "name": "organizer"},
                {"id": 2, "name": "coorganizer"},
            ],
            "links": {"next": None},
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_event_roles(event_id)

        self.client.session.get.assert_called_once()
        args, kwargs = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("events/1/roles"))
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0].name, "organizer")
        self.assertEqual(result.data[1].name, "coorganizer")

    def test_get_role(self):
        event_id = "1"
        role_id = "1"
        expected = {
            "data": {
                "id": 1,
                "name": "organizer",
                "title_name": "Organizer",
            }
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_role(event_id, role_id)

        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("events/1/roles/1"))
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "organizer")
        self.assertEqual(result.title_name, "Organizer")


if __name__ == "__main__":
    unittest.main()
