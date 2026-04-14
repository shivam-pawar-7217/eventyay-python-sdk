"""Tests for Track-related operations."""

from eventyay.models import Track, TrackList


class TestGetEventTracks:
    def test_returns_track_list(self, mock_client, mock_response, sample_track):
        mock_client.session.get.return_value = mock_response({"data": [sample_track]})

        result = mock_client.get_event_tracks("test-event")

        assert isinstance(result, TrackList)
        assert len(result.data) == 1
        assert result.data[0].name == "AI & ML"
        assert result.data[0].color == "#3498db"


class TestGetTrack:
    def test_returns_track(self, mock_client, mock_response, sample_track):
        mock_client.session.get.return_value = mock_response(sample_track)

        result = mock_client.get_track("test-event", "501")

        assert isinstance(result, Track)
        assert result.name == "AI & ML"
