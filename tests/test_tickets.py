import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Ticket, TicketList

class TestTicketsAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_ticket_data = {
            "id": 1,
            "name": "General Admission",
            "type": "paid",
            "price": 50.00,
            "quantity": 100,
            "is_hidden": False
        }
    
    @patch('eventyay.client.requests.Session.get')
    def test_get_event_tickets(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [self.mock_ticket_data, {"id": 2, "name": "VIP", "type": "paid", "price": 100.0, "quantity": 50}],
            "meta": {"total": 2}
        }
        mock_get.return_value = mock_response

        # Call the method
        tickets_list = self.client.get_event_tickets("test-event", page=1, page_size=10)

        # Assertions
        self.assertIsInstance(tickets_list, TicketList)
        self.assertEqual(len(tickets_list.data), 2)
        
        first_ticket = tickets_list.data[0]
        self.assertIsInstance(first_ticket, Ticket)
        self.assertEqual(first_ticket.id, 1)
        self.assertEqual(first_ticket.name, "General Admission")
        self.assertEqual(first_ticket.price, 50.00)
        
        # Verify the correct URL and params were called
        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/tickets", 
            params={'page': 1, 'page_size': 10}
        )

    @patch('eventyay.client.requests.Session.get')
    def test_get_ticket(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_ticket_data
        mock_get.return_value = mock_response

        # Call the method
        ticket = self.client.get_ticket("test-event", "1")

        # Assertions
        self.assertIsInstance(ticket, Ticket)
        self.assertEqual(ticket.id, 1)
        self.assertEqual(ticket.name, "General Admission")

        # Verify the correct URL was called
        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/tickets/1", 
            params=None
        )

if __name__ == '__main__':
    unittest.main()
