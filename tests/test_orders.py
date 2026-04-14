"""Tests for Order-related operations."""

from eventyay.models import Order, OrderList


class TestGetEventOrders:
    def test_returns_order_list(self, mock_client, mock_response, sample_order):
        mock_client.session.get.return_value = mock_response({"data": [sample_order]})

        result = mock_client.get_event_orders("test-event")

        assert isinstance(result, OrderList)
        assert len(result.data) == 1
        assert result.data[0].identifier == "ORD-001"
        assert result.data[0].status == "completed"
        assert result.data[0].amount == 50.0


class TestGetOrder:
    def test_returns_order(self, mock_client, mock_response, sample_order):
        mock_client.session.get.return_value = mock_response(sample_order)

        result = mock_client.get_order("test-event", "ORD-001")

        assert isinstance(result, Order)
        assert result.paid_via == "stripe"
