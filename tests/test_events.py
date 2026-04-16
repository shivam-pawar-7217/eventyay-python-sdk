"""Tests for Event-related operations."""

from unittest.mock import Mock

from eventyay.models import Event, EventList


class TestGetEvent:
    def test_returns_event_model(self, mock_client, mock_response, sample_event):
        mock_client.session.get.return_value = mock_response(sample_event)

        result = mock_client.get_event(1)

        assert isinstance(result, Event)
        assert result.id == 1
        assert result.name == "Test Conference"
        assert result.identifier == "test-conf-2026"

    def test_calls_correct_endpoint(self, mock_client, mock_response, sample_event):
        mock_client.session.get.return_value = mock_response(sample_event)

        mock_client.get_event(42)

        args, _ = mock_client.session.get.call_args
        assert args[0].endswith("events/42")


class TestGetEvents:
    def test_returns_event_list(self, mock_client, mock_response, sample_event):
        mock_client.session.get.return_value = mock_response({"data": [sample_event]})

        result = mock_client.get_events()

        assert isinstance(result, EventList)
        assert len(result.data) == 1
        assert result.data[0].name == "Test Conference"

    def test_pagination_params(self, mock_client, mock_response, sample_event):
        mock_client.session.get.return_value = mock_response({"data": [sample_event]})

        mock_client.get_events(page=2, page_size=20)

        _, kwargs = mock_client.session.get.call_args
        assert kwargs["params"]["page[number]"] == 2
        assert kwargs["params"]["page[size]"] == 20

    def test_calls_non_trailing_slash_endpoint(self, mock_client, mock_response, sample_event):
        mock_client.session.get.return_value = mock_response({"data": [sample_event]})

        mock_client.get_events()

        args, _ = mock_client.session.get.call_args
        assert args[0].endswith("/events")

    def test_nullable_boolean_fields_are_coerced(self, mock_client, mock_response, sample_event):
        event_with_null_bools = {
            **sample_event,
            "stream_loop": None,
            "stream_autoplay": None,
            "is_badges_enabled": None,
            "is_ticket_form_enabled": None,
        }
        mock_client.session.get.return_value = mock_response({"data": [event_with_null_bools]})

        result = mock_client.get_events()

        event = result.data[0]
        assert event.stream_loop is False
        assert event.stream_autoplay is False
        assert event.is_badges_enabled is True
        assert event.is_ticket_form_enabled is True


class TestGetAllEvents:
    def test_fetches_all_pages(self, mock_client, mock_response, sample_event):
        page1 = mock_response(
            {"data": [sample_event], "links": {"next": "http://api/events?page=2"}}
        )
        page2 = mock_response(
            {"data": [{**sample_event, "id": 2, "name": "Second Event"}], "links": {"next": None}}
        )
        mock_client.session.get.side_effect = [page1, page2]

        result = mock_client.get_all_events()

        assert len(result) == 2
        assert result[0].name == "Test Conference"
        assert result[1].name == "Second Event"

    def test_stops_on_empty_data(self, mock_client, mock_response):
        mock_client.session.get.return_value = mock_response({"data": []})

        result = mock_client.get_all_events()

        assert result == []


class TestGetEventAttendees:
    def test_returns_attendee_list(self, mock_client, mock_response, sample_attendee):
        mock_client.session.get.return_value = mock_response({"data": [sample_attendee]})

        result = mock_client.get_event_attendees("test-event")

        assert len(result.data) == 1
        assert result.data[0].email == "alice@test.com"

    def test_correct_endpoint(self, mock_client, mock_response, sample_attendee):
        mock_client.session.get.return_value = mock_response({"data": [sample_attendee]})

        mock_client.get_event_attendees("my-event")

        args, _ = mock_client.session.get.call_args
        assert "events/my-event/attendees" in args[0]


class TestGetEventSessions:
    def test_returns_session_list(self, mock_client, mock_response, sample_session):
        mock_client.session.get.return_value = mock_response({"data": [sample_session]})

        result = mock_client.get_event_sessions("test-event")

        assert len(result.data) == 1
        assert result.data[0].title == "Keynote: Future of Open Source"


class TestGetEventSpeakers:
    def test_returns_speaker_list(self, mock_client, mock_response, sample_speaker):
        mock_client.session.get.return_value = mock_response({"data": [sample_speaker]})

        result = mock_client.get_event_speakers("test-event")

        assert len(result.data) == 1
        assert result.data[0].name == "Dr. Jane Doe"


class TestCreateEvent:
    def test_creates_event(self, mock_client, mock_response, sample_event):
        mock_client.session.post.return_value = mock_response(sample_event)

        result = mock_client.create_event(
            name="Test Conference",
            identifier="test-conf-2026",
            starts_at="2026-06-01T09:00:00Z",
            ends_at="2026-06-03T18:00:00Z",
            timezone="UTC",
        )

        assert isinstance(result, Event)
        assert result.name == "Test Conference"
        mock_client.session.post.assert_called_once()


class TestUpdateEvent:
    def test_updates_event(self, mock_client, mock_response, sample_event):
        updated = {**sample_event, "name": "Updated Conference"}
        mock_client.session.patch.return_value = mock_response(updated)

        result = mock_client.update_event(event_id=1, name="Updated Conference")

        assert result.name == "Updated Conference"

    def test_no_update_returns_current(self, mock_client, mock_response, sample_event):
        mock_client.session.get.return_value = mock_response(sample_event)

        result = mock_client.update_event(event_id=1)

        assert result.name == "Test Conference"
        mock_client.session.get.assert_called_once()


class TestDeleteEvent:
    def test_deletes_event(self, mock_client):
        response = Mock()
        response.status_code = 204
        mock_client.session.delete.return_value = response

        result = mock_client.delete_event(1)

        assert result is True
        mock_client.session.delete.assert_called_once()
