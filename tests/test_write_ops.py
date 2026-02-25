import unittest
from unittest.mock import Mock
from eventyay.client import EventyayClient


class TestWriteOperations(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test-key")
        self.client.session = Mock()

    def test_create_organizer(self):
        # Arrange
        name = "New Org"
        expected_response = {"id": 1, "name": name, "description": "Desc"}
        mock_response = Mock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 201
        self.client.session.post.return_value = mock_response

        # Act
        result = self.client.create_organizer(name=name, description="Desc")

        # Assert
        self.client.session.post.assert_called_once()
        args, kwargs = self.client.session.post.call_args
        self.assertTrue(args[0].endswith("organizers"))
        self.assertEqual(kwargs["json"]["name"], name)
        self.assertEqual(result.id, 1)

    def test_update_organizer(self):
        # Arrange
        org_id = "1"
        new_name = "Updated Org"
        expected_response = {"id": 1, "name": new_name}
        mock_response = Mock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 200
        self.client.session.patch.return_value = mock_response

        # Act
        result = self.client.update_organizer(org_id, name=new_name)

        # Assert
        self.client.session.patch.assert_called_once()
        args, kwargs = self.client.session.patch.call_args
        self.assertTrue(args[0].endswith(f"organizers/{org_id}"))
        self.assertEqual(kwargs["json"]["name"], new_name)
        self.assertEqual(result.name, new_name)

    def test_delete_organizer(self):
        # Arrange
        org_id = "1"
        mock_response = Mock()
        mock_response.status_code = 204  # No Content
        self.client.session.delete.return_value = mock_response

        # Act
        result = self.client.delete_organizer(org_id)

        # Assert
        self.client.session.delete.assert_called_once()
        self.assertTrue(result)

    def test_create_event(self):
        # Arrange
        name = "New Event"
        identifier = "new-event"
        starts_at = "2026-01-01T10:00:00"
        ends_at = "2026-01-01T18:00:00"
        timezone = "UTC"
        expected_response = {
            "id": 101,
            "name": name,
            "identifier": identifier,
            "starts_at": starts_at,
        }
        mock_response = Mock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 201
        self.client.session.post.return_value = mock_response

        # Act
        result = self.client.create_event(
            name=name,
            identifier=identifier,
            starts_at=starts_at,
            ends_at=ends_at,
            timezone=timezone,
        )

        # Assert
        self.client.session.post.assert_called_once()
        args, kwargs = self.client.session.post.call_args
        self.assertTrue(args[0].endswith("events"))
        self.assertEqual(kwargs["json"]["identifier"], identifier)
        self.assertEqual(result.id, 101)


if __name__ == "__main__":
    unittest.main()
