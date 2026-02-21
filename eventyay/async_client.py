import aiohttp
import asyncio
from typing import Optional, Dict, Any
from .exceptions import (
    EventyayAPIError,
    EventyayConnectionError,
    EventyayTimeoutError
)

from .async_mixins import (
    AsyncOrganizersMixin, AsyncEventsMixin, 
    AsyncTicketsMixin, AsyncAttendeesMixin
)

class AsyncEventyayClient(AsyncOrganizersMixin, AsyncEventsMixin, AsyncTicketsMixin, AsyncAttendeesMixin):
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
        """Async GET request with automatic retries for rate limits."""
        return await self._request('GET', endpoint, params=params)
            
    async def _post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async POST request."""
        return await self._request('POST', endpoint, json=json)

    async def _patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async PATCH request."""
        return await self._request('PATCH', endpoint, json=json)

    async def _delete(self, endpoint: str) -> None:
        """Async DELETE request."""
        await self._request('DELETE', endpoint)

    async def _request(self, method: str, endpoint: str, 
                        params: Optional[Dict[str, Any]] = None,
                        json: Optional[Dict[str, Any]] = None) -> Any:
        """Internal helper for async requests with retry logic."""
        if not self._session:
            self._session = aiohttp.ClientSession(headers=self.headers)
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        max_retries = 3
        backoff = 1
        
        for attempt in range(max_retries + 1):
            try:
                async with self._session.request(method, url, params=params, json=json) as response:
                    if response.status == 429 and attempt < max_retries:
                        wait_time = backoff * (2 ** attempt)
                        await asyncio.sleep(wait_time)
                        continue
                    
                    if method == 'DELETE' and response.status == 204:
                        return None
                        
                    response.raise_for_status()
                    if method == 'DELETE':
                        return None
                    return await response.json()
            except aiohttp.ClientError as e:
                if attempt == max_retries:
                    raise EventyayConnectionError(f"Async {method} request failed: {e}")
                await asyncio.sleep(backoff * (2 ** attempt))
            
