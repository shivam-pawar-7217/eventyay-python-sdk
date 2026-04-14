"""Tests for Speaker-related operations."""

from eventyay.models import Speaker


class TestGetSpeaker:
    def test_returns_speaker(self, mock_client, mock_response, sample_speaker):
        mock_client.session.get.return_value = mock_response(sample_speaker)

        result = mock_client.get_speaker("test-event", "201")

        assert isinstance(result, Speaker)
        assert result.name == "Dr. Jane Doe"
        assert result.email == "jane@speaker.com"

    def test_correct_endpoint(self, mock_client, mock_response, sample_speaker):
        mock_client.session.get.return_value = mock_response(sample_speaker)

        mock_client.get_speaker("my-event", "5")

        args, _ = mock_client.session.get.call_args
        assert "events/my-event/speakers/5" in args[0]
