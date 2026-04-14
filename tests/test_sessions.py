"""Tests for Session-related operations."""

from eventyay.models import Session


class TestGetSession:
    def test_returns_session(self, mock_client, mock_response, sample_session):
        mock_client.session.get.return_value = mock_response(sample_session)

        result = mock_client.get_session("test-event", "301")

        assert isinstance(result, Session)
        assert result.title == "Keynote: Future of Open Source"

    def test_correct_endpoint(self, mock_client, mock_response, sample_session):
        mock_client.session.get.return_value = mock_response(sample_session)

        mock_client.get_session("my-event", "10")

        args, _ = mock_client.session.get.call_args
        assert "events/my-event/sessions/10" in args[0]
