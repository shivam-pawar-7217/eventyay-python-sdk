import aiohttp
import asyncio
from typing import Optional, Dict, Any
from .exceptions import (
    EventyayAPIError,
    EventyayConnectionError,
    EventyayTimeoutError
)

class AsyncEventyayClient:
    """
    Asynchronous client for the Eventyay API.
    Uses aiohttp for non-blocking I/O.
    """
    
    def __init__(
        self,
        base_url: str = "https://dev.eventyay.com/api/v1",
        api_key: Optional[str] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Token {api_key}'
            
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def get_events(self):
        """Fetch events asynchronously."""
        if not self._session:
            self._session = aiohttp.ClientSession(headers=self.headers)
            
        url = f"{self.base_url}/events"
        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            raise EventyayConnectionError(f"Async request failed: {e}")
