"""Tests for Ticket Tag related operations."""

from eventyay.models import TicketTag, TicketTagList


class TestGetEventTicketTags:
    def test_returns_ticket_tag_list(self, mock_client, mock_response, sample_ticket_tag):
        mock_client.session.get.return_value = mock_response({"data": [sample_ticket_tag]})

        result = mock_client.get_event_ticket_tags("test-event")

        assert isinstance(result, TicketTagList)
        assert len(result.data) == 1
        assert result.data[0].name == "VIP"


class TestGetTicketTag:
    def test_returns_ticket_tag(self, mock_client, mock_response, sample_ticket_tag):
        mock_client.session.get.return_value = mock_response(sample_ticket_tag)

        result = mock_client.get_ticket_tag("1451")

        assert isinstance(result, TicketTag)
        assert result.color == "#ff8800"
