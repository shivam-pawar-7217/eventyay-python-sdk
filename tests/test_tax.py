"""Tests for Tax-related operations."""

from eventyay.models import Tax


class TestGetEventTax:
    def test_returns_tax(self, mock_client, mock_response, sample_tax):
        mock_client.session.get.return_value = mock_response(sample_tax)

        result = mock_client.get_event_tax("test-event")

        assert isinstance(result, Tax)
        assert result.name == "GST"
        assert result.rate == 18.0
        assert result.is_tax_included_in_price is False
        assert result.country == "IN"

    def test_correct_endpoint(self, mock_client, mock_response, sample_tax):
        mock_client.session.get.return_value = mock_response(sample_tax)

        mock_client.get_event_tax("my-event")

        args, _ = mock_client.session.get.call_args
        assert "events/my-event/tax" in args[0]

    def test_get_tax_alias(self, mock_client, mock_response, sample_tax):
        mock_client.session.get.return_value = mock_response(sample_tax)

        result = mock_client.get_tax("my-event")

        assert isinstance(result, Tax)
        args, _ = mock_client.session.get.call_args
        assert "events/my-event/tax" in args[0]
