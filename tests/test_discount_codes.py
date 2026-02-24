import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import DiscountCode, DiscountCodeList


class TestDiscountCodesAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_code_data = {
            "id": 1,
            "code": "EARLYBIRD",
            "discount_url": "https://example.com/earlybird",
            "value": 20.0,
            "type": "percent",
            "is_active": True,
            "tickets_number": 100,
            "min_quantity": 1,
            "max_quantity": 10,
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_till": "2026-06-01T00:00:00Z",
        }

    @patch("eventyay.client.requests.Session.get")
    def test_get_event_discount_codes(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                self.mock_code_data,
                {
                    "id": 2,
                    "code": "VIP50",
                    "value": 50.0,
                    "type": "percent",
                    "is_active": True,
                },
            ],
            "meta": {"total": 2},
        }
        mock_get.return_value = mock_response

        result = self.client.get_event_discount_codes(
            "test-event", page=1, page_size=10
        )

        self.assertIsInstance(result, DiscountCodeList)
        self.assertEqual(len(result.data), 2)

        first = result.data[0]
        self.assertIsInstance(first, DiscountCode)
        self.assertEqual(first.id, 1)
        self.assertEqual(first.code, "EARLYBIRD")
        self.assertEqual(first.value, 20.0)
        self.assertTrue(first.is_active)

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/" "events/test-event/discount-codes",
            params={"page": 1, "page_size": 10},
        )

    @patch("eventyay.client.requests.Session.get")
    def test_get_discount_code(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_code_data
        mock_get.return_value = mock_response

        result = self.client.get_discount_code("test-event", "1")

        self.assertIsInstance(result, DiscountCode)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.code, "EARLYBIRD")
        self.assertEqual(result.type, "percent")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/" "events/test-event/discount-codes/1",
            params=None,
        )


if __name__ == "__main__":
    unittest.main()
