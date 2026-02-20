import os
import unittest
import uuid
from eventyay import EventyayClient
from eventyay.exceptions import EventyayAPIError

class TestRealAPIIntegration(unittest.TestCase):
    """
    Integration tests against the live Eventyay API.
    These tests require a valid API KEY set in the EVENTYAY_API_KEY environment variable.
    WARNING: These tests will create and delete real data on the server.
    """

    @classmethod
    def setUpClass(cls):
        cls.api_key = os.environ.get('EVENTYAY_API_KEY')
        if not cls.api_key:
            raise unittest.SkipTest("EVENTYAY_API_KEY not set. Skipping integration tests.")
        
        cls.client = EventyayClient(api_key=cls.api_key)
        cls.unique_suffix = str(uuid.uuid4())[:8]

    def test_full_event_lifecycle(self):
        """Test creating, fetching, updating, and deleting an organizer and event."""
        # 1. Create Organizer
        org_name = f"Test Org {self.unique_suffix}"
        print(f"\nCreating organizer: {org_name}")
        organizer = self.client.create_organizer(name=org_name, description="Integration Test")
        self.assertIsNotNone(organizer.id)
        
        # 2. Create Event for Organizer
        event_name = f"Test Event {self.unique_suffix}"
        print(f"Creating event: {event_name}")
        event = self.client.create_event(
            name=event_name,
            identifier=f"test-event-{self.unique_suffix}",
            starts_at="2027-01-01T10:00:00Z",
            ends_at="2027-01-01T12:00:00Z",
            timezone="UTC"
        )
        self.assertIsNotNone(event.id)

        # 3. Update Event
        print(f"Updating event ID: {event.id}")
        updated_event = self.client.update_event(
            event.id,
            name=f"{event_name} (Updated)"
        )
        self.assertEqual(updated_event.name, f"{event_name} (Updated)")

        # 4. Fetch Event
        print(f"Fetching event ID: {event.id}")
        fetched_event = self.client.get_event(event.id)
        self.assertEqual(fetched_event.id, event.id)

        # 5. Cleanup (Delete)
        print(f"Deleting event ID: {event.id}")
        self.client.delete_event(event.id)
        
        print(f"Deleting organizer ID: {organizer.id}")
        self.client.delete_organizer(organizer.id)

if __name__ == '__main__':
    unittest.main()
