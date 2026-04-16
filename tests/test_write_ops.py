"""Tests for write operations (create, update, delete) across domains."""

from unittest.mock import Mock

from eventyay.models import Organizer


class TestWriteOperations:
    """Test POST, PATCH, DELETE operations use correct HTTP methods and endpoints."""

    def test_post_uses_correct_method(self, mock_client, mock_response, sample_event):
        mock_client.session.post.return_value = mock_response(sample_event)

        mock_client.create_event(
            name="Test",
            identifier="test",
            starts_at="2026-01-01T00:00:00Z",
            ends_at="2026-01-02T00:00:00Z",
            timezone="UTC",
        )

        mock_client.session.post.assert_called_once()
        args, kwargs = mock_client.session.post.call_args
        assert args[0].endswith("events")
        assert kwargs["json"]["data"]["attributes"]["name"] == "Test"

    def test_patch_uses_correct_method(self, mock_client, mock_response, sample_event):
        updated = {**sample_event, "name": "Updated"}
        mock_client.session.patch.return_value = mock_response(updated)

        mock_client.update_event(event_id=1, name="Updated")

        mock_client.session.patch.assert_called_once()
        args, kwargs = mock_client.session.patch.call_args
        assert "events/1" in args[0]

    def test_post_supports_idempotency_key(self, mock_client, mock_response, sample_event):
        mock_client.session.post.return_value = mock_response(sample_event)

        mock_client.create_event(
            name="Test",
            identifier="test",
            starts_at="2026-01-01T00:00:00Z",
            ends_at="2026-01-02T00:00:00Z",
            timezone="UTC",
            idempotency_key="idem-123",
        )

        _, kwargs = mock_client.session.post.call_args
        assert kwargs["headers"]["Idempotency-Key"] == "idem-123"

    def test_patch_supports_idempotency_key(self, mock_client, mock_response, sample_event):
        mock_client.session.patch.return_value = mock_response(sample_event)

        mock_client.update_event(event_id=1, name="Updated", idempotency_key="idem-456")

        _, kwargs = mock_client.session.patch.call_args
        assert kwargs["headers"]["Idempotency-Key"] == "idem-456"

    def test_delete_uses_correct_method(self, mock_client):
        response = Mock()
        response.status_code = 204
        mock_client.session.delete.return_value = response

        mock_client.delete_event(1)

        mock_client.session.delete.assert_called_once()
        args, _ = mock_client.session.delete.call_args
        assert "events/1" in args[0]

    def test_organizer_create(self, mock_client, mock_response, sample_organizer):
        mock_client.session.post.return_value = mock_response(sample_organizer)

        result = mock_client.create_organizer(name="FOSSASIA")

        assert isinstance(result, Organizer)
        mock_client.session.post.assert_called_once()

    def test_organizer_delete(self, mock_client):
        response = Mock()
        response.status_code = 204
        mock_client.session.delete.return_value = response

        result = mock_client.delete_organizer("fossasia")

        assert result is True
