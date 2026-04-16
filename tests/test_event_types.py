"""Tests for Event Type related operations."""

from eventyay.models import EventType, EventTypeList


class TestGetEventTypes:
    def test_returns_event_type_list(self, mock_client, mock_response, sample_event_type):
        mock_client.session.get.return_value = mock_response({"data": [sample_event_type]})

        result = mock_client.get_event_types()

        assert isinstance(result, EventTypeList)
        assert len(result.data) == 1
        assert result.data[0].name == "conference"


class TestGetEventType:
    def test_returns_event_type(self, mock_client, mock_response, sample_event_type):
        mock_client.session.get.return_value = mock_response(sample_event_type)

        result = mock_client.get_event_type("1601")

        assert isinstance(result, EventType)
        assert result.id == 1601
