import unittest
from unittest.mock import Mock
import requests
from eventyay.client import EventyayClient
from eventyay.exceptions import EventyayConnectionError, EventyayTimeoutError

class TestErrors(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_connection_error(self):
        # Simulate a ConnectionError from requests
        self.client.session.get.side_effect = requests.exceptions.ConnectionError("No internet")
        
        with self.assertRaises(EventyayConnectionError):
            self.client._get("events")

    def test_timeout_error(self):
        # Simulate a Timeout from requests
        self.client.session.get.side_effect = requests.exceptions.Timeout("Timed out")
        
        with self.assertRaises(EventyayTimeoutError):
            self.client._get("events")

    def test_post_connection_error(self):
        # Verify that POST also handles connection errors
        self.client.session.post.side_effect = requests.exceptions.ConnectionError("No internet")
        
        with self.assertRaises(EventyayConnectionError):
            self.client._post("events", data={})

if __name__ == '__main__':
    unittest.main()
