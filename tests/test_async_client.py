import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from eventyay.async_client import AsyncEventyayClient
from eventyay.exceptions import EventyayTimeoutError, EventyayRateLimitError
from eventyay.models import (
    Organizer,
    OrganizerList,
    Event,
    EventList,
    Attendee,
    AttendeeList,
    Ticket,
    TicketList,
    Speaker,
    Session,
    Track,
    TrackList,
    Microlocation,
    MicrolocationList,
    Sponsor,
    SponsorList,
    DiscountCode,
    DiscountCodeList,
    User,
    UserList,
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

    @patch("aiohttp.ClientSession.request")
    async def test_get_organizers(self, mock_request):
        """Test fetching organizers asynchronously."""
        mock_data = {"data": [{"id": 1, "name": "Test Org"}], "links": {}, "meta": {}}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_organizers()
        self.assertIsInstance(result, OrganizerList)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].name, "Test Org")

    @patch("aiohttp.ClientSession.request")
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

    @patch("aiohttp.ClientSession.request")
    async def test_get_events(self, mock_request):
        """Test fetching a list of events (Async)."""
        mock_data = {
            "data": [{"id": 100, "name": "PyCon", "identifier": "pycon"}],
            "links": {},
            "meta": {},
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_events()
        self.assertIsInstance(result, EventList)
        self.assertEqual(result.data[0].name, "PyCon")

    @patch("aiohttp.ClientSession.request")
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

    @patch("aiohttp.ClientSession.request")
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
        self.assertEqual(args[0], "POST")

    @patch("aiohttp.ClientSession.request")
    async def test_delete_event(self, mock_request):
        """Test deleting an event asynchronously."""
        mock_resp = MagicMock()
        mock_resp.status = 204
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.delete_event(100)
        self.assertTrue(result)
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "DELETE")

    # -------------------------------------------------------------
    # TICKETS
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_event_tickets(self, mock_request):
        mock_ticket_data = {
            "data": [{"id": 1, "name": "Early Bird", "type": "paid", "price": 10.0}]
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

    @patch("aiohttp.ClientSession.request")
    async def test_get_ticket(self, mock_request):
        mock_ticket_data = {
            "id": 1,
            "name": "Early Bird",
            "type": "paid",
            "price": 10.0,
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
    @patch("aiohttp.ClientSession.request")
    async def test_get_event_attendees(self, mock_request):
        mock_attendee_data = {
            "data": [
                {
                    "id": 1,
                    "email": "test@example.com",
                    "firstname": "Async",
                    "lastname": "Coder",
                }
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

    @patch("aiohttp.ClientSession.request")
    async def test_get_attendee(self, mock_request):
        mock_attendee_data = {
            "id": 1,
            "email": "test@example.com",
            "firstname": "Async",
            "lastname": "Coder",
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

    # -------------------------------------------------------------
    # SPEAKERS
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_speaker(self, mock_request):
        mock_speaker_data = {
            "id": 1,
            "name": "Async Speaker",
            "short_biography": "Expert",
        }

        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_speaker_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_speaker("event-1", "1")

        self.assertIsInstance(result, Speaker)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Async Speaker")

    # -------------------------------------------------------------
    # SESSIONS
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_session(self, mock_request):
        mock_session_data = {
            "id": 101,
            "title": "Async Session",
            "starts_at": "2026-02-22",
        }

        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_session_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp

        result = await self.client.get_session("event-1", "101")

        self.assertIsInstance(result, Session)
        self.assertEqual(result.id, 101)
        self.assertEqual(result.title, "Async Session")

    # -------------------------------------------------------------
    # TRACKS
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_event_tracks(self, mock_request):
        mock_data = {
            "data": [{"id": 1, "name": "AI Track", "color": "#FF0000"}],
            "meta": {"total": 1},
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_event_tracks("event-1")
        self.assertIsInstance(result, TrackList)
        self.assertEqual(len(result.data), 1)

    @patch("aiohttp.ClientSession.request")
    async def test_get_track(self, mock_request):
        mock_data = {"id": 1, "name": "AI Track"}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_track("event-1", "1")
        self.assertIsInstance(result, Track)
        self.assertEqual(result.name, "AI Track")

    # -------------------------------------------------------------
    # MICROLOCATIONS
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_event_microlocations(self, mock_request):
        mock_data = {
            "data": [{"id": 1, "name": "Main Hall", "floor": 1}],
            "meta": {"total": 1},
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_event_microlocations("event-1")
        self.assertIsInstance(result, MicrolocationList)

    @patch("aiohttp.ClientSession.request")
    async def test_get_microlocation(self, mock_request):
        mock_data = {"id": 1, "name": "Room A", "floor": 2}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_microlocation("event-1", "1")
        self.assertIsInstance(result, Microlocation)
        self.assertEqual(result.name, "Room A")

    # -------------------------------------------------------------
    # SPONSORS
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_event_sponsors(self, mock_request):
        mock_data = {
            "data": [{"id": 1, "name": "TechCorp", "level": "Gold"}],
            "meta": {"total": 1},
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_event_sponsors("event-1")
        self.assertIsInstance(result, SponsorList)

    @patch("aiohttp.ClientSession.request")
    async def test_get_sponsor(self, mock_request):
        mock_data = {"id": 1, "name": "TechCorp", "level": "Gold"}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_sponsor("event-1", "1")
        self.assertIsInstance(result, Sponsor)
        self.assertEqual(result.name, "TechCorp")

    # -------------------------------------------------------------
    # DISCOUNT CODES
    # -------------------------------------------------------------
    @patch("aiohttp.ClientSession.request")
    async def test_get_event_discount_codes(self, mock_request):
        mock_data = {
            "data": [{"id": 1, "code": "SAVE20", "value": 20.0}],
            "meta": {"total": 1},
        }
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_event_discount_codes("event-1")
        self.assertIsInstance(result, DiscountCodeList)

    @patch("aiohttp.ClientSession.request")
    async def test_get_discount_code(self, mock_request):
        mock_data = {"id": 1, "code": "SAVE20", "type": "percent"}
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value.__aenter__.return_value = mock_resp
        result = await self.client.get_discount_code("event-1", "1")
        self.assertIsInstance(result, DiscountCode)
        self.assertEqual(result.code, "SAVE20")

    # --- Users API ---

    @patch("aiohttp.ClientSession.request")
    async def test_get_users(self, mock_request):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": 1,
                    "email": "async@test.com",
                    "first_name": "Async",
                    "last_name": "User",
                }
            ],
            "links": {"next": None},
            "meta": {"count": 1},
        }
        mock_request.return_value.__aenter__.return_value = mock_response

        async with AsyncEventyayClient(api_key="test") as client:
            users = await client.get_users(page=1, page_size=10)

        self.assertIsInstance(users, UserList)
        self.assertEqual(len(users.data), 1)
        self.assertEqual(users.data[0].email, "async@test.com")
        self.assertEqual(users.data[0].id, 1)

    @patch("aiohttp.ClientSession.request")
    async def test_get_user(self, mock_request):
        user_id = "1"
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "email": "async@test.com",
            }
        }
        mock_request.return_value.__aenter__.return_value = mock_response

        async with AsyncEventyayClient(api_key="test") as client:
            user = await client.get_user(user_id)

        self.assertIsInstance(user, User)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "async@test.com")


if __name__ == "__main__":
    unittest.main()
