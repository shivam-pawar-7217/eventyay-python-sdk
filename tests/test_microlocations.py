"""Tests for Microlocation-related operations."""

from eventyay.models import Microlocation, MicrolocationList


class TestGetEventMicrolocations:
    def test_returns_microlocation_list(self, mock_client, mock_response, sample_microlocation):
        mock_client.session.get.return_value = mock_response({"data": [sample_microlocation]})

        result = mock_client.get_event_microlocations("test-event")

        assert isinstance(result, MicrolocationList)
        assert len(result.data) == 1
        assert result.data[0].name == "Main Hall"
        assert result.data[0].floor == 1


class TestGetMicrolocation:
    def test_returns_microlocation(self, mock_client, mock_response, sample_microlocation):
        mock_client.session.get.return_value = mock_response(sample_microlocation)

        result = mock_client.get_microlocation("test-event", "601")

        assert isinstance(result, Microlocation)
        assert result.room == "A101"
