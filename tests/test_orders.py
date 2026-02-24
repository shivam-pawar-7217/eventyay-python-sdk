import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Order, OrderList


class TestOrdersAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_order_data = {
            "id": 1,
            "identifier": "ORD-001",
            "status": "completed",
            "amount": 49.99,
            "paid_via": "stripe",
            "created_at": "2026-02-20T10:00:00Z",
            "completed_at": "2026-02-20T10:05:00Z",
        }

    @patch("eventyay.client.requests.Session.get")
    def test_get_event_orders(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                self.mock_order_data,
                {
                    "id": 2,
                    "identifier": "ORD-002",
                    "status": "pending",
                    "amount": 0.0,
                    "paid_via": "free",
                },
            ],
            "meta": {"total": 2},
        }
        mock_get.return_value = mock_response

        result = self.client.get_event_orders("test-event", page=1, page_size=10)

        self.assertIsInstance(result, OrderList)
        self.assertEqual(len(result.data), 2)

        first = result.data[0]
        self.assertIsInstance(first, Order)
        self.assertEqual(first.id, 1)
        self.assertEqual(first.identifier, "ORD-001")
        self.assertEqual(first.status, "completed")
        self.assertEqual(first.amount, 49.99)
        self.assertEqual(first.paid_via, "stripe")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/" "events/test-event/orders",
            params={"page": 1, "page_size": 10},
        )

    @patch("eventyay.client.requests.Session.get")
    def test_get_order(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_order_data
        mock_get.return_value = mock_response

        result = self.client.get_order("test-event", "ORD-001")

        self.assertIsInstance(result, Order)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.identifier, "ORD-001")
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.amount, 49.99)

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/" "events/test-event/orders/ORD-001",
            params=None,
        )

    @patch("eventyay.client.requests.Session.get")
    def test_get_event_orders_empty(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"total": 0}}
        mock_get.return_value = mock_response

        result = self.client.get_event_orders("empty-event")

        self.assertIsInstance(result, OrderList)
        self.assertEqual(len(result.data), 0)

    def test_order_str(self):
        order = Order(id=1, identifier="ORD-001", status="completed")
        self.assertEqual(
            str(order), "Order(id=1, identifier='ORD-001', status='completed')"
        )


if __name__ == "__main__":
    unittest.main()
