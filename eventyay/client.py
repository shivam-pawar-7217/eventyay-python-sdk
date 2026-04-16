"""
Eventyay API Client

Main client class for interacting with the Eventyay REST API.
Provides synchronous access with automatic retries, error mapping,
JSON:API response parsing, and configurable timeouts.
"""

from typing import Any, Dict, NoReturn, Optional, cast

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .attendees import AttendeesMixin
from .access_codes import AccessCodesMixin
from .auth import AuthMixin
from .discount_codes import DiscountCodesMixin
from .events import EventsMixin
from .event_sub_topics import EventSubTopicsMixin
from .event_topics import EventTopicsMixin
from .event_types import EventTypesMixin
from .exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayConnectionError,
    EventyayNotFoundError,
    EventyayRateLimitError,
    EventyayTimeoutError,
    EventyayValidationError,
)
from .feedbacks import FeedbacksMixin
from .microlocations import MicrolocationsMixin
from .misc_resources import MiscResourcesMixin
from .notifications import NotificationsMixin
from .orders import OrdersMixin
from .operations import OperationsMixin
from .organizers import OrganizersMixin
from .pages import PagesMixin
from .role_invites import RoleInvitesMixin
from .roles import RolesMixin
from .sessions import SessionsMixin
from .services import ServicesMixin
from .settings import SettingsMixin
from .speakers import SpeakersMixin
from .sponsors import SponsorsMixin
from .tax import TaxMixin
from .tickets import TicketsMixin
from .ticket_tags import TicketTagsMixin
from .tracks import TracksMixin
from .users import UsersMixin
from .utils import validate_endpoint_path


class EventyayClient(
    AuthMixin,
    OrganizersMixin,
    EventsMixin,
    EventTypesMixin,
    EventTopicsMixin,
    EventSubTopicsMixin,
    TicketsMixin,
    TicketTagsMixin,
    AttendeesMixin,
    SpeakersMixin,
    SessionsMixin,
    TracksMixin,
    MicrolocationsMixin,
    SponsorsMixin,
    DiscountCodesMixin,
    AccessCodesMixin,
    NotificationsMixin,
    PagesMixin,
    ServicesMixin,
    OrdersMixin,
    TaxMixin,
    UsersMixin,
    RolesMixin,
    RoleInvitesMixin,
    FeedbacksMixin,
    SettingsMixin,
    MiscResourcesMixin,
    OperationsMixin,
):
    """
    The primary entry point for interacting with the Eventyay REST API.

    This client combines multiple mixins to provide a unified interface for
    managing organizers, events, tickets, and more. It handles authentication,
    retries, and error mapping automatically.

    Example:
        ```python
        from eventyay import EventyayClient

        client = EventyayClient(api_key="your_api_key")
        events = client.get_events()
        for event in events.data:
            print(event.name)
        ```

    Can also be used as a context manager:
        ```python
        with EventyayClient(api_key="your_key") as client:
            events = client.get_events()
        ```

    Attributes:
        base_url (str): The base URL of the Eventyay API.
        api_key (Optional[str]): Your Eventyay API key for authenticated requests.
        timeout (int): Request timeout in seconds.
        session (requests.Session): The underlying requests session with retry logic.
    """

    def __init__(
        self,
        base_url: str = "https://api.eventyay.com/v1",
        api_key: Optional[str] = None,
        auth_mode: str = "token",
        timeout: int = 30,
        max_retries: int = 3,
        strict_jsonapi: bool = False,
    ):
        """
        Initializes the EventyayClient.

        Args:
            base_url (str, optional): The API base URL.
                Defaults to the production server.
            api_key (str, optional): Your API key or JWT access token.
                If omitted, only public endpoints work.
            auth_mode (str, optional): Authentication mode — either
                'token' (API key) or 'jwt' (access token). Defaults to 'token'.
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
            max_retries (int, optional): Maximum retry attempts for failed requests.
                Defaults to 3.
            strict_jsonapi (bool, optional): Enforce strict JSON:API wrapper shape
                in parser utilities. Defaults to False.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.auth_mode = auth_mode.lower()
        self.timeout = timeout
        self.strict_jsonapi = strict_jsonapi
        self.session = requests.Session()

        # Configure Retries (Reliability)
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,  # 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["HEAD", "GET", "OPTIONS"]),
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # Set up authentication header
        # JSON:API server supports both JWT and Token auth
        if api_key:
            if self.auth_mode == "jwt":
                self.session.headers["Authorization"] = f"JWT {api_key}"
            else:
                self.session.headers["Authorization"] = f"Token {api_key}"

        # JSON:API spec Content-Type
        self.session.headers.update(
            {
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json",
            }
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        """Close the underlying requests session and release connections."""
        self.session.close()

    def __repr__(self):
        masked_key = f"{self.api_key[:4]}..." if self.api_key else "None"
        return (
            f"EventyayClient(base_url='{self.base_url}', "
            f"api_key='{masked_key}', timeout={self.timeout})"
        )

    def __str__(self):
        return self.__repr__()

    def _safe_json(self, response: requests.Response) -> Dict[str, Any]:
        """Parse successful response JSON and raise a typed SDK error on malformed bodies."""
        try:
            data = response.json()
            if not isinstance(data, dict):
                raise EventyayAPIError(
                    "Server returned a non-object JSON payload in a successful response.",
                    status_code=response.status_code,
                )
            return cast(Dict[str, Any], data)
        except ValueError as e:
            raise EventyayAPIError(
                "Server returned malformed JSON in a successful response.",
                status_code=response.status_code,
            ) from e

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs a GET request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint path (e.g., 'events').
            params (dict, optional): Query parameters to include.

        Returns:
            Dict[str, Any]: The parsed JSON response data.

        Raises:
            EventyayAPIError: If the request fails or the server returns an error.
            EventyayAuthenticationError: If the API key is missing or invalid.
            EventyayNotFoundError: If the requested resource does not exist.
        """
        safe_endpoint = validate_endpoint_path(endpoint)
        url = f"{self.base_url}/{safe_endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return self._safe_json(response)
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError(
                "Could not connect to the Eventyay API. " "Please check your internet connection."
            )
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError(
                f"The request to the Eventyay API timed out after {self.timeout}s."
            )
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")

    def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Performs a POST request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint path.
            json (dict, optional): The JSON payload for the request.
            idempotency_key (str, optional): Value for the `Idempotency-Key` header.

        Returns:
            Dict[str, Any]: The parsed JSON response data.
        """
        safe_endpoint = validate_endpoint_path(endpoint)
        url = f"{self.base_url}/{safe_endpoint}"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None

        try:
            response = self.session.post(url, json=json, timeout=self.timeout, headers=headers)
            response.raise_for_status()
            return self._safe_json(response)
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError(
                "Could not connect to the Eventyay API. " "Please check your internet connection."
            )
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError(
                f"The request to the Eventyay API timed out after {self.timeout}s."
            )
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")

    def _patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Performs a PATCH request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint path.
            json (dict, optional): The JSON payload (partial update).

        Returns:
            Dict[str, Any]: The parsed JSON response data.
        """
        safe_endpoint = validate_endpoint_path(endpoint)
        url = f"{self.base_url}/{safe_endpoint}"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None

        try:
            response = self.session.patch(url, json=json, timeout=self.timeout, headers=headers)
            response.raise_for_status()
            return self._safe_json(response)
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError(
                "Could not connect to the Eventyay API. " "Please check your internet connection."
            )
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError(
                f"The request to the Eventyay API timed out after {self.timeout}s."
            )
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")

    def _delete(self, endpoint: str) -> None:
        """
        Performs a DELETE request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint path.

        Raises:
            EventyayAPIError: If deletion fails.
        """
        safe_endpoint = validate_endpoint_path(endpoint)
        url = f"{self.base_url}/{safe_endpoint}"

        try:
            response = self.session.delete(url, timeout=self.timeout)
            # 204 No Content is common for delete
            if response.status_code == 204:
                return
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError(
                "Could not connect to the Eventyay API. " "Please check your internet connection."
            )
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError(
                f"The request to the Eventyay API timed out after {self.timeout}s."
            )
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")

    def _handle_error(self, response: requests.Response) -> NoReturn:
        """
        Maps HTTP error responses to SDK-specific exceptions.

        Args:
            response (requests.Response): The failing response object.
        """
        status_code = response.status_code
        response_body = response.text

        try:
            error_data = response.json()
            error_message = error_data.get("detail") or error_data.get("message") or str(error_data)
        except ValueError:
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
                f"Rate limit exceeded. Try again later. {error_message}",
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
