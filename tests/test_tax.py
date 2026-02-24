import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Tax


class TestTaxAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_tax_data = {
            "id": 1,
            "name": "GST",
            "rate": 18.0,
            "is_tax_included_in_price": True,
            "country": "IN",
        }

    @patch("eventyay.client.requests.Session.get")
    def test_get_event_tax(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_tax_data
        mock_get.return_value = mock_response

        result = self.client.get_event_tax("test-event")

        self.assertIsInstance(result, Tax)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "GST")
        self.assertEqual(result.rate, 18.0)
        self.assertTrue(result.is_tax_included_in_price)
        self.assertEqual(result.country, "IN")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/" "events/test-event/tax", params=None
        )

    @patch("eventyay.client.requests.Session.get")
    def test_get_event_tax_minimal(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 2, "name": "VAT"}
        mock_get.return_value = mock_response

        result = self.client.get_event_tax("another-event")

        self.assertIsInstance(result, Tax)
        self.assertEqual(result.id, 2)
        self.assertEqual(result.name, "VAT")
        self.assertIsNone(result.rate)
        self.assertFalse(result.is_tax_included_in_price)

    def test_tax_str(self):
        tax = Tax(id=1, name="GST", rate=18.0)
        self.assertEqual(str(tax), "Tax(id=1, name='GST', rate=18.0%)")


if __name__ == "__main__":
    unittest.main()
