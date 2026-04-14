"""Tests for DiscountCode-related operations."""

from eventyay.models import DiscountCode, DiscountCodeList


class TestGetEventDiscountCodes:
    def test_returns_discount_code_list(self, mock_client, mock_response, sample_discount_code):
        mock_client.session.get.return_value = mock_response({"data": [sample_discount_code]})

        result = mock_client.get_event_discount_codes("test-event")

        assert isinstance(result, DiscountCodeList)
        assert len(result.data) == 1
        assert result.data[0].code == "EARLYBIRD"
        assert result.data[0].value == 20.0
        assert result.data[0].is_active is True


class TestGetDiscountCode:
    def test_returns_discount_code(self, mock_client, mock_response, sample_discount_code):
        mock_client.session.get.return_value = mock_response(sample_discount_code)

        result = mock_client.get_discount_code("test-event", "801")

        assert isinstance(result, DiscountCode)
        assert result.type == "percent"
