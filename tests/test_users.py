import unittest
from unittest.mock import Mock
from eventyay.client import EventyayClient


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_get_users(self):
        expected = {
            "data": [
                {
                    "id": 1,
                    "email": "test1@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                }
            ],
            "links": {"next": "https://api.example.com/v1/users?page=2"},
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_users(page=1, page_size=25)

        self.client.session.get.assert_called_once()
        args, kwargs = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("users"))
        self.assertEqual(kwargs["params"]["page[number]"], 1)
        self.assertEqual(kwargs["params"]["page[size]"], 25)

        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].id, 1)
        self.assertEqual(result.data[0].email, "test1@example.com")
        self.assertEqual(
            result.links["next"], "https://api.example.com/v1/users?page=2"
        )

    def test_get_user(self):
        user_id = "1"
        expected = {
            "data": {
                "id": 1,
                "email": "test1@example.com",
                "first_name": "Jon",
            }
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_user(user_id)

        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("users/1"))

        self.assertEqual(result.id, 1)
        self.assertEqual(result.first_name, "Jon")

    def test_update_user(self):
        user_id = "1"
        update_payload = {"first_name": "UpdatedName"}
        expected = {
            "data": {
                "id": 1,
                "email": "test1@example.com",
                "first_name": "UpdatedName",
            }
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.patch.return_value = mock_response

        result = self.client.update_user(user_id, update_payload)

        self.client.session.patch.assert_called_once()
        args, kwargs = self.client.session.patch.call_args
        self.assertTrue(args[0].endswith("users/1"))

        # Verify JSON payload structure for JSON API
        sent_json = kwargs["json"]
        self.assertEqual(sent_json["data"]["type"], "user")
        self.assertEqual(sent_json["data"]["id"], "1")
        self.assertEqual(sent_json["data"]["attributes"]["first_name"], "UpdatedName")

        self.assertEqual(result.id, 1)
        self.assertEqual(result.first_name, "UpdatedName")


if __name__ == "__main__":
    unittest.main()
