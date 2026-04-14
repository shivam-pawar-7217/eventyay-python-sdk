"""Tests for Ticket-related operations."""

from eventyay.models import Ticket, TicketList


class TestGetEventTickets:
    def test_returns_ticket_list(self, mock_client, mock_response, sample_ticket):
        mock_client.session.get.return_value = mock_response({"data": [sample_ticket]})

        result = mock_client.get_event_tickets("test-event")

        assert isinstance(result, TicketList)
        assert len(result.data) == 1
        assert result.data[0].name == "General Admission"
        assert result.data[0].price == 25.0

    def test_correct_endpoint(self, mock_client, mock_response, sample_ticket):
        mock_client.session.get.return_value = mock_response({"data": [sample_ticket]})

        mock_client.get_event_tickets("my-event")

        args, _ = mock_client.session.get.call_args
        assert "events/my-event/tickets" in args[0]


class TestGetTicket:
    def test_returns_ticket(self, mock_client, mock_response, sample_ticket):
        mock_client.session.get.return_value = mock_response(sample_ticket)

        result = mock_client.get_ticket("test-event", "401")

        assert isinstance(result, Ticket)
        assert result.type == "paid"
