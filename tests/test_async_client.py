import pytest
from unittest.mock import AsyncMock, patch
from eventyay.async_client import AsyncEventyayClient

@pytest.mark.asyncio
async def test_get_organizers():
    # Mock the response
    mock_response_data = [{"id": 1, "name": "Organizer 1"}]
    
    # Mock aiohttp session
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json.return_value = mock_response_data
        
        # Context manager mock
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        client = AsyncEventyayClient()
        organizers = await client.get_organizers()
        
        assert len(organizers) == 1
        assert organizers[0]['name'] == "Organizer 1"

@pytest.mark.asyncio
async def test_get_events():
    mock_response_data = [{"id": 100, "name": "Event 1"}]
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json.return_value = mock_response_data
        
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        client = AsyncEventyayClient()
        events = await client.get_events()
        
        assert len(events) == 1
        assert events[0]['name'] == "Event 1"
