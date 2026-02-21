import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from eventyay.async_client import AsyncEventyayClient
from eventyay.exceptions import EventyayTimeoutError, EventyayRateLimitError
from eventyay.models import (
    Organizer, OrganizerList,
    Event, EventList, Attendee, AttendeeList,
    Ticket, TicketList
)

class TestAsyncClient(unittest.IsolatedAsyncioTestCase):
    """
    Asynchronous tests for the Eventyay SDK.
    Using IsolatedAsyncioTestCase for compatibility with unittest discovery.
    """

    async def asyncSetUp(self):
        self.client = AsyncEventyayClient(api_key="test_token")

    async def asyncTearDown(self):
        await self.client.__aexit__(None, None, None)

    @patch('aiohttp.ClientSession.request')
    async def test_get_organizers(self, mock_request):
        """Test fetching organizers asynchronously."""
        mock_data = {
            "data": [{"id": 1, "name": "Test Org"}],
            "links": {},
            "meta": {}
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_organizers()
        self.assertIsInstance(result, OrganizerList)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].name, "Test Org")

    @patch('aiohttp.ClientSession.request')
    async def test_get_organizer_detail(self, mock_request):
        """Test fetching a single organizer by ID (Async)."""
        mock_data = {"id": 1, "name": "Test Org"}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_organizer("1")
        self.assertIsInstance(result, Organizer)
        self.assertEqual(result.id, 1)

    @patch('aiohttp.ClientSession.request')
    async def test_get_events(self, mock_request):
        """Test fetching a list of events (Async)."""
        mock_data = {
            "data": [{"id": 100, "name": "PyCon", "identifier": "pycon"}],
            "links": {},
            "meta": {}
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_events()
        self.assertIsInstance(result, EventList)
        self.assertEqual(result.data[0].name, "PyCon")

    @patch('aiohttp.ClientSession.request')
    async def test_get_event_detail(self, mock_request):
        """Test fetching a single event (Async)."""
        mock_data = {"id": 100, "name": "PyCon", "identifier": "pycon"}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_event(100)
        self.assertIsInstance(result, Event)
        self.assertEqual(result.id, 100)

    @patch('aiohttp.ClientSession.request')
    async def test_create_organizer(self, mock_request):
        """Test creating an organizer asynchronously."""
        mock_data = {"id": 1, "name": "New Org"}
        mock_resp = MagicMock()
        mock_resp.status = 201
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.create_organizer(name="New Org")
        self.assertEqual(result.name, "New Org")
        mock_request.assert_called_once()
        # Verify it was a POST request
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], 'POST')

    @patch('aiohttp.ClientSession.request')
    async def test_delete_event(self, mock_request):
        """Test deleting an event asynchronously."""
        mock_resp = MagicMock()
        mock_resp.status = 204
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.delete_event(100)
        self.assertTrue(result)
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], 'DELETE')

    # -------------------------------------------------------------
    # TICKETS
    # -------------------------------------------------------------
    @patch('aiohttp.ClientSession.request')
    async def test_get_event_tickets(self, mock_request):
        mock_ticket_data = {
            "data": [
                {"id": 1, "name": "Early Bird", "type": "paid", "price": 10.0}
            ]
        }
        
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_ticket_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        
        result = await self.client.get_event_tickets("event-1")
        
        self.assertIsInstance(result, TicketList)
        self.assertEqual(len(result.data), 1)
        self.assertIsInstance(result.data[0], Ticket)
        self.assertEqual(result.data[0].id, 1)

    @patch('aiohttp.ClientSession.request')
    async def test_get_ticket(self, mock_request):
        mock_ticket_data = {
             "id": 1, "name": "Early Bird", "type": "paid", "price": 10.0
        }
        
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_ticket_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        
        result = await self.client.get_ticket("event-1", "1")
        
        self.assertIsInstance(result, Ticket)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Early Bird")

    # -------------------------------------------------------------
    # ATTENDEES
    # -------------------------------------------------------------
    @patch('aiohttp.ClientSession.request')
    async def test_get_event_attendees(self, mock_request):
        mock_attendee_data = {
            "data": [
                {"id": 1, "email": "test@example.com", "firstname": "Async", "lastname": "Coder"}
            ]
        }
        
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_attendee_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        
        result = await self.client.get_event_attendees("event-1")
        
        self.assertIsInstance(result, AttendeeList)
        self.assertEqual(len(result.data), 1)
        self.assertIsInstance(result.data[0], Attendee)
        self.assertEqual(result.data[0].id, 1)

    @patch('aiohttp.ClientSession.request')
    async def test_get_attendee(self, mock_request):
        mock_attendee_data = {
             "id": 1, "email": "test@example.com", "firstname": "Async", "lastname": "Coder"
        }
        
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_attendee_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        
        result = await self.client.get_attendee("event-1", "1")
        
        self.assertIsInstance(result, Attendee)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.firstname, "Async")

if __name__ == '__main__':
    unittest.main()
