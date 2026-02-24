import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Attendee, AttendeeList


class TestAttendeesAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_attendee_data = {
            "id": 1,
            "email": "test@example.com",
            "firstname": "John",
            "lastname": "Doe",
            "isCheckedIn": False,
        }

    @patch("eventyay.client.requests.Session.get")
    def test_get_event_attendees(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                self.mock_attendee_data,
                {
                    "id": 2,
                    "email": "jane@example.com",
                    "firstname": "Jane",
                    "lastname": "Smith",
                    "isCheckedIn": True,
                },
            ],
            "meta": {"total": 2},
        }
        mock_get.return_value = mock_response

        # Call the method
        attendee_list = self.client.get_event_attendees(
            "test-event", page=1, page_size=10
        )

        # Assertions
        self.assertIsInstance(attendee_list, AttendeeList)
        self.assertEqual(len(attendee_list.data), 2)

        first_attendee = attendee_list.data[0]
        self.assertIsInstance(first_attendee, Attendee)
        self.assertEqual(first_attendee.id, 1)
        self.assertEqual(first_attendee.email, "test@example.com")
        self.assertFalse(first_attendee.isCheckedIn)

        # Verify the correct URL and params were called
        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/attendees",
            params={"page": 1, "page_size": 10},
        )

    @patch("eventyay.client.requests.Session.get")
    def test_get_attendee(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_attendee_data
        mock_get.return_value = mock_response

        # Call the method
        attendee = self.client.get_attendee("test-event", "1")

        # Assertions
        self.assertIsInstance(attendee, Attendee)
        self.assertEqual(attendee.id, 1)
        self.assertEqual(attendee.firstname, "John")

        # Verify the correct URL was called
        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/attendees/1", params=None
        )


if __name__ == "__main__":
    unittest.main()
