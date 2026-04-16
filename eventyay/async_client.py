"""
Eventyay Async API Client

Asynchronous client for the Eventyay REST API using aiohttp.
Provides full feature parity with the synchronous client, including
automatic retries with exponential backoff and proper error mapping.
"""

import asyncio
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Dict, NoReturn, Optional, cast

import aiohttp

from .async_mixins import (
    AsyncAccessCodesMixin,
    AsyncAuthMixin,
    AsyncAttendeesMixin,
    AsyncDiscountCodesMixin,
    AsyncEventsMixin,
    AsyncEventSubTopicsMixin,
    AsyncEventTopicsMixin,
    AsyncEventTypesMixin,
    AsyncFeedbacksMixin,
    AsyncMicrolocationsMixin,
    AsyncMiscResourcesMixin,
    AsyncNotificationsMixin,
    AsyncOperationsMixin,
    AsyncOrdersMixin,
    AsyncOrganizersMixin,
    AsyncPagesMixin,
    AsyncRoleInvitesMixin,
    AsyncRolesMixin,
    AsyncSessionsMixin,
    AsyncServicesMixin,
    AsyncSettingsMixin,
    AsyncSpeakersMixin,
    AsyncSponsorsMixin,
    AsyncTaxMixin,
    AsyncTicketsMixin,
    AsyncTicketTagsMixin,
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
from .utils import validate_endpoint_path


class AsyncEventyayClient(
    AsyncAuthMixin,
    AsyncOrganizersMixin,
    AsyncEventsMixin,
    AsyncEventTypesMixin,
    AsyncEventTopicsMixin,
    AsyncEventSubTopicsMixin,
    AsyncTicketsMixin,
    AsyncTicketTagsMixin,
    AsyncAttendeesMixin,
    AsyncSpeakersMixin,
    AsyncSessionsMixin,
    AsyncTracksMixin,
    AsyncMicrolocationsMixin,
    AsyncSponsorsMixin,
    AsyncDiscountCodesMixin,
    AsyncAccessCodesMixin,
    AsyncNotificationsMixin,
    AsyncPagesMixin,
    AsyncServicesMixin,
    AsyncOrdersMixin,
    AsyncTaxMixin,
    AsyncUsersMixin,
    AsyncRolesMixin,
    AsyncRoleInvitesMixin,
    AsyncFeedbacksMixin,
    AsyncSettingsMixin,
    AsyncMiscResourcesMixin,
    AsyncOperationsMixin,
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
        base_url: str = "https://api.eventyay.com/v1",
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        strict_jsonapi: bool = False,
    ):
        """
        Initializes the AsyncEventyayClient.

        Args:
            base_url: The API base URL.
            api_key: Your API key. If omitted, only public endpoints work.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Maximum retry attempts. Defaults to 3.
            strict_jsonapi: Enforce strict JSON:API wrapper shape in parser
                utilities. Defaults to False.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.strict_jsonapi = strict_jsonapi
        self.headers: Dict[str, str] = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }
        if api_key:
            self.headers["Authorization"] = f"Token {api_key}"

        self._session: Optional[aiohttp.ClientSession] = None
        self._session_loop: Optional[asyncio.AbstractEventLoop] = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure a live session exists and is bound to the currently running event loop."""
        running_loop = asyncio.get_running_loop()

        needs_new_session = (
            self._session is None
            or self._session.closed
            or self._session_loop is not running_loop
        )

        if needs_new_session:
            if self._session is not None and not self._session.closed:
                await self._session.close()

            connector = aiohttp.TCPConnector(limit=100, enable_cleanup_closed=True)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                headers=self.headers,
                connector=connector,
                timeout=timeout,
            )
            self._session_loop = running_loop

        session = self._session
        assert session is not None
        return session

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the underlying aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None
            self._session_loop = None

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
        return cast(Dict[str, Any], await self._request("GET", endpoint, params=params))

    async def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Async POST request."""
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return cast(Dict[str, Any], await self._request("POST", endpoint, json=json, headers=headers))

    async def _patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Async PATCH request."""
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return cast(Dict[str, Any], await self._request("PATCH", endpoint, json=json, headers=headers))

    async def _delete(self, endpoint: str) -> None:
        """Async DELETE request."""
        await self._request("DELETE", endpoint)

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Internal helper for async requests with retry logic and error mapping."""
        safe_endpoint = validate_endpoint_path(endpoint)
        session = await self._ensure_session()

        url = f"{self.base_url}/{safe_endpoint}"
        backoff = 1
        is_safe_method = method.upper() in {"GET", "HEAD", "OPTIONS"}

        for attempt in range(self.max_retries + 1):
            try:
                async with session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=headers,
                ) as response:
                    should_retry, wait_time, result = await self._process_response(
                        method=method,
                        response=response,
                        attempt=attempt,
                        backoff=backoff,
                        is_safe_method=is_safe_method,
                    )
                    if should_retry:
                        await asyncio.sleep(wait_time)
                        continue
                    return result

            except (EventyayAPIError,):
                raise
            except asyncio.TimeoutError:
                if not self._should_retry_exception(attempt, is_safe_method):
                    raise EventyayTimeoutError(
                        f"Async request timed out after {self.timeout}s.",
                        status_code=None,
                    )
                await asyncio.sleep(backoff * (2**attempt))
            except aiohttp.ClientError as e:
                if not self._should_retry_exception(attempt, is_safe_method):
                    raise EventyayConnectionError(
                        f"Async {method} request failed: {e}",
                        status_code=None,
                    )
                await asyncio.sleep(backoff * (2**attempt))

    async def _process_response(
        self,
        method: str,
        response: aiohttp.ClientResponse,
        attempt: int,
        backoff: int,
        is_safe_method: bool,
    ) -> tuple[bool, float, Any]:
        """Process a response and decide whether to retry or return a parsed result."""
        if self._should_retry_response(response.status, attempt, is_safe_method):
            wait_time = self._get_retry_delay(response, attempt, backoff)
            return True, wait_time, None

        # Successful DELETE returns no content.
        if method == "DELETE" and response.status == 204:
            return False, 0.0, None

        if response.status >= 400:
            await self._handle_error(response)

        # Successful response for DELETE (non-204)
        if method == "DELETE":
            return False, 0.0, None

        return False, 0.0, await self._safe_json(response)

    def _should_retry_response(self, status_code: int, attempt: int, is_safe_method: bool) -> bool:
        """Return True when status-based retry policy should trigger."""
        if attempt >= self.max_retries or not is_safe_method:
            return False
        return status_code == 429 or status_code in (500, 502, 503, 504)

    def _should_retry_exception(self, attempt: int, is_safe_method: bool) -> bool:
        """Return True when exception-based retry policy should trigger."""
        return is_safe_method and attempt < self.max_retries

    def _get_retry_delay(
        self,
        response: aiohttp.ClientResponse,
        attempt: int,
        backoff: int,
    ) -> float:
        """Honor Retry-After when present, otherwise use exponential backoff."""
        default_delay = float(backoff * (2**attempt))
        retry_after = response.headers.get("Retry-After")
        if not retry_after:
            return default_delay

        try:
            return max(float(retry_after), 0.0)
        except ValueError:
            try:
                retry_dt = parsedate_to_datetime(retry_after)
                if retry_dt.tzinfo is None:
                    retry_dt = retry_dt.replace(tzinfo=timezone.utc)
                return max((retry_dt - datetime.now(timezone.utc)).total_seconds(), 0.0)
            except Exception:
                return default_delay

    async def _safe_json(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Parse successful response JSON and raise a typed SDK error on malformed bodies."""
        try:
            data = await response.json(content_type=None)
            if not isinstance(data, dict):
                raise EventyayAPIError(
                    "Server returned a non-object JSON payload in a successful response.",
                    status_code=response.status,
                )
            return cast(Dict[str, Any], data)
        except Exception as e:
            raise EventyayAPIError(
                "Server returned malformed JSON in a successful response.",
                status_code=response.status,
            ) from e

    async def _handle_error(self, response: aiohttp.ClientResponse) -> NoReturn:
        """Map async HTTP error responses to SDK-specific exceptions."""
        status_code = response.status
        response_body = await response.text()

        try:
            error_data = await response.json(content_type=None)
            if isinstance(error_data, dict):
                error_message = error_data.get("detail") or error_data.get("message") or str(error_data)
            else:
                error_message = str(error_data)
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
