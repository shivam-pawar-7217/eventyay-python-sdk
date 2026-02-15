import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from eventyay.async_client import AsyncEventyayClient


@pytest.mark.asyncio
async def test_get_organizers():
    """Test fetching all organizers asynchronously."""
    mock_data = [{"id": 1, "name": "Test Org"}]

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_organizers()
        assert result == mock_data


@pytest.mark.asyncio
async def test_get_organizer_detail():
    """Test fetching a single organizer by ID."""
    mock_data = {"id": 1, "name": "Test Org", "slug": "test-org"}

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_organizer("1")
        assert result["slug"] == "test-org"


@pytest.mark.asyncio
async def test_get_events():
    """Test fetching all events asynchronously."""
    mock_data = [{"id": 100, "name": "PyCon"}]

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_events()
        assert len(result) == 1
        assert result[0]["name"] == "PyCon"


@pytest.mark.asyncio
async def test_get_event_detail():
    """Test fetching a single event by ID."""
    mock_data = {"id": 100, "name": "PyCon", "location": "Pittsburgh"}

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_event(100)
        assert result["location"] == "Pittsburgh"


@pytest.mark.asyncio
async def test_get_event_attendees():
    """Test fetching attendees for an event."""
    mock_data = [{"id": 1, "email": "test@example.com"}]

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_event_attendees("100")
        assert result[0]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_event_speakers():
    """Test fetching speakers for an event."""
    mock_data = [{"id": 1, "name": "Guido van Rossum"}]

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_event_speakers("100")
        assert result[0]["name"] == "Guido van Rossum"


@pytest.mark.asyncio
async def test_get_event_sessions():
    """Test fetching sessions for an event."""
    mock_data = [{"id": 1, "title": "Keynote: Python 4.0"}]

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_resp

        client = AsyncEventyayClient()
        result = await client.get_event_sessions("100")
        assert result[0]["title"] == "Keynote: Python 4.0"
