"""Tests for Attendee-related operations."""

from eventyay.models import Attendee, AttendeeList


class TestGetEventAttendees:
    def test_returns_attendee_list(self, mock_client, mock_response, sample_attendee):
        mock_client.session.get.return_value = mock_response({"data": [sample_attendee]})

        result = mock_client.get_event_attendees("test-event")

        assert isinstance(result, AttendeeList)
        assert len(result.data) == 1
        assert result.data[0].email == "alice@test.com"
        assert result.data[0].isCheckedIn is True

    def test_correct_endpoint(self, mock_client, mock_response, sample_attendee):
        mock_client.session.get.return_value = mock_response({"data": [sample_attendee]})

        mock_client.get_event_attendees("my-event")

        args, _ = mock_client.session.get.call_args
        assert "events/my-event/attendees" in args[0]


class TestGetAttendee:
    def test_returns_attendee(self, mock_client, mock_response, sample_attendee):
        mock_client.session.get.return_value = mock_response(sample_attendee)

        result = mock_client.get_attendee("test-event", "101")

        assert isinstance(result, Attendee)
        assert result.firstname == "Alice"
        assert result.lastname == "Smith"
