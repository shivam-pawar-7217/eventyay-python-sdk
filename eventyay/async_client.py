"""
Eventyay Async API Client

Asynchronous client for the Eventyay REST API using aiohttp.
Provides full feature parity with the synchronous client, including
automatic retries with exponential backoff and proper error mapping.
"""

import asyncio
from typing import Any, Dict, Optional

import aiohttp

from .async_mixins import (
    AsyncAttendeesMixin,
    AsyncDiscountCodesMixin,
    AsyncEventsMixin,
    AsyncFeedbacksMixin,
    AsyncMicrolocationsMixin,
    AsyncOrdersMixin,
    AsyncOrganizersMixin,
    AsyncRolesMixin,
    AsyncSessionsMixin,
    AsyncSettingsMixin,
    AsyncSpeakersMixin,
    AsyncSponsorsMixin,
    AsyncTaxMixin,
    AsyncTicketsMixin,
    AsyncTracksMixin,
    AsyncUsersMixin,
)
from .exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayConnectionError,
    EventyayNotFoundError,
    EventyayRateLimitError,
    EventyayTimeoutError,
    EventyayValidationError,
)


class AsyncEventyayClient(
    AsyncOrganizersMixin,
    AsyncEventsMixin,
    AsyncTicketsMixin,
    AsyncAttendeesMixin,
    AsyncSpeakersMixin,
    AsyncSessionsMixin,
    AsyncTracksMixin,
    AsyncMicrolocationsMixin,
    AsyncSponsorsMixin,
    AsyncDiscountCodesMixin,
    AsyncOrdersMixin,
    AsyncTaxMixin,
    AsyncUsersMixin,
    AsyncRolesMixin,
    AsyncFeedbacksMixin,
    AsyncSettingsMixin,
):
    """
    Asynchronous client for the Eventyay API.

    Uses aiohttp for non-blocking I/O with automatic retries
    and exponential backoff for rate limits and server errors.

    Example:
        ```python
        async with AsyncEventyayClient(api_key="your_key") as client:
            events = await client.get_events()
            for event in events.data:
                print(event.name)
        ```

    Attributes:
        base_url (str): The base URL of the Eventyay API.
        api_key (Optional[str]): Your Eventyay API key.
        timeout (int): Request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str = "https://dev.eventyay.com/api/v1",
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initializes the AsyncEventyayClient.

        Args:
            base_url: The API base URL.
            api_key: Your API key. If omitted, only public endpoints work.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Maximum retry attempts. Defaults to 3.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if api_key:
            self.headers["Authorization"] = f"Token {api_key}"

        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the underlying aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None

    def __repr__(self):
        masked_key = f"{self.api_key[:4]}..." if self.api_key else "None"
        return (
            f"AsyncEventyayClient(base_url='{self.base_url}', "
            f"api_key='{masked_key}', timeout={self.timeout})"
        )

    def __str__(self):
        return self.__repr__()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async GET request with automatic retries for rate limits."""
        return await self._request("GET", endpoint, params=params)

    async def _post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async POST request."""
        return await self._request("POST", endpoint, json=json)

    async def _patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async PATCH request."""
        return await self._request("PATCH", endpoint, json=json)

    async def _delete(self, endpoint: str) -> None:
        """Async DELETE request."""
        await self._request("DELETE", endpoint)

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Internal helper for async requests with retry logic and error mapping."""
        if not self._session:
            self._session = aiohttp.ClientSession(headers=self.headers)

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        backoff = 1
        client_timeout = aiohttp.ClientTimeout(total=self.timeout)

        for attempt in range(self.max_retries + 1):
            try:
                async with self._session.request(
                    method, url, params=params, json=json, timeout=client_timeout
                ) as response:
                    # Retry on rate limit
                    if response.status == 429 and attempt < self.max_retries:
                        wait_time = backoff * (2**attempt)
                        await asyncio.sleep(wait_time)
                        continue

                    # Retry on server errors
                    if response.status in (500, 502, 503, 504) and attempt < self.max_retries:
                        wait_time = backoff * (2**attempt)
                        await asyncio.sleep(wait_time)
                        continue

                    # Successful DELETE returns no content
                    if method == "DELETE" and response.status == 204:
                        return None

                    # Handle error responses
                    if response.status >= 400:
                        await self._handle_error(response)

                    # Successful response for DELETE (non-204)
                    if method == "DELETE":
                        return None

                    return await response.json()

            except (EventyayAPIError,):
                raise
            except asyncio.TimeoutError:
                if attempt == self.max_retries:
                    raise EventyayTimeoutError(
                        f"Async request timed out after {self.timeout}s.",
                        status_code=None,
                    )
                await asyncio.sleep(backoff * (2**attempt))
            except aiohttp.ClientError as e:
                if attempt == self.max_retries:
                    raise EventyayConnectionError(
                        f"Async {method} request failed: {e}",
                        status_code=None,
                    )
                await asyncio.sleep(backoff * (2**attempt))

    async def _handle_error(self, response: aiohttp.ClientResponse) -> None:
        """Map async HTTP error responses to SDK-specific exceptions."""
        status_code = response.status
        response_body = await response.text()

        try:
            error_data = await response.json()
            error_message = error_data.get("detail") or error_data.get("message") or str(error_data)
        except Exception:
            error_message = response_body or f"HTTP {status_code} error"

        if status_code in (401, 403):
            raise EventyayAuthenticationError(
                error_message,
                status_code=status_code,
                response_body=response_body,
            )
        if status_code == 404:
            raise EventyayNotFoundError(
                error_message,
                status_code=status_code,
                response_body=response_body,
            )
        if status_code == 429:
            raise EventyayRateLimitError(
                f"Rate limit exceeded. {error_message}",
                status_code=status_code,
                response_body=response_body,
            )
        if 400 <= status_code < 500:
            raise EventyayValidationError(
                error_message,
                status_code=status_code,
                response_body=response_body,
            )
        else:
            raise EventyayAPIError(
                f"HTTP {status_code}: {error_message}",
                status_code=status_code,
                response_body=response_body,
            )
