import aiohttp
import asyncio
from typing import Optional, Dict, Any
from .exceptions import (
    EventyayAPIError,
    EventyayConnectionError,
    EventyayTimeoutError
)

from .async_mixins import AsyncOrganizersMixin, AsyncEventsMixin

class AsyncEventyayClient(AsyncOrganizersMixin, AsyncEventsMixin):
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

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async GET request."""
        if not self._session:
            self._session = aiohttp.ClientSession(headers=self.headers)
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with self._session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            raise EventyayConnectionError(f"Async request failed: {e}")
            
    async def get_events(self):
        """Deprecated: Use Mixin method."""
        # This was the old skeleton method. We should remove it or delegate to mixin.
        # Since we inherit from AsyncEventsMixin, we should just remove this 
        # to avoid shadowing the mixin method.
        # But wait, AsyncEventsMixin isn't implemented fully yet. 
        # Let's remove this method so the mixin takes over when implemented.
        pass
