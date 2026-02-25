import unittest
from unittest.mock import Mock
from eventyay.client import EventyayClient


class TestFeedbacks(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_get_event_feedbacks(self):
        event_id = "1"
        expected = {
            "data": [
                {"id": 1, "rating": 4.5, "comment": "Great!"},
                {"id": 2, "rating": 3.0, "comment": "OK"},
            ],
            "links": {"next": None},
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_event_feedbacks(event_id)

        self.client.session.get.assert_called_once()
        args, kwargs = self.client.session.get.call_args
        self.assertIn("events/1/feedbacks", args[0])
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0].rating, 4.5)
        self.assertEqual(result.data[1].comment, "OK")

    def test_get_feedback(self):
        event_id = "1"
        feedback_id = "1"
        expected = {
            "data": {
                "id": 1,
                "rating": 5.0,
                "comment": "Excellent session!",
                "session_id": 10,
            }
        }

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_feedback(event_id, feedback_id)

        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertIn("events/1/feedbacks/1", args[0])
        self.assertEqual(result.id, 1)
        self.assertEqual(result.rating, 5.0)
        self.assertEqual(result.session_id, 10)


if __name__ == "__main__":
    unittest.main()
