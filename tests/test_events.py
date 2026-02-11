import unittest
from unittest.mock import Mock
from eventyay.client import EventyayClient

class TestEvents(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_get_event(self):
        event_id = "1"
        expected = {"id": "1", "name": "Test Event"}
        
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_event(event_id)
        
        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("events/1"))
        self.assertEqual(result, expected)

    def test_get_event_attendees(self):
        event_id = "1"
        expected = [{"id": "101", "name": "Attendee 1"}]
        
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_event_attendees(event_id)
        
        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("events/1/attendees"))
        self.assertEqual(result, expected)

    def test_get_event_sessions(self):
        event_id = "1"
        expected = [{"id": "201", "title": "Talk 1"}]
        
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_event_sessions(event_id)
        
        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("events/1/sessions"))
        self.assertEqual(result, expected)

    def test_get_event_speakers(self):
        event_id = "1"
        expected = [{"id": "301", "name": "Speaker 1"}]
        
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.status_code = 200
        self.client.session.get.return_value = mock_response

        result = self.client.get_event_speakers(event_id)
        
        self.client.session.get.assert_called_once()
        args, _ = self.client.session.get.call_args
        self.assertTrue(args[0].endswith("events/1/speakers"))
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
