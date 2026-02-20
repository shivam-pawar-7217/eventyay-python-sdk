"""
Eventyay API Client

Main client class for interacting with the Eventyay REST API.
"""

import requests
from typing import Optional, Dict, Any
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayNotFoundError,
    EventyayValidationError,
    EventyayConnectionError,
    EventyayTimeoutError,
    EventyayRateLimitError
)


from .organizers import OrganizersMixin
from .events import EventsMixin

class EventyayClient(OrganizersMixin, EventsMixin):
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

    Attributes:
        base_url (str): The base URL of the Eventyay API (e.g., https://api.eventyay.com/v1).
        api_key (Optional[str]): Your Eventyay API key for authenticated requests.
        session (requests.Session): The underlying requests session with retry logic.
    """
    
    def __init__(
        self,
        base_url: str = "https://dev.eventyay.com/api/v1",
        api_key: Optional[str] = None
    ):
        """
        Initializes the EventyayClient.

        Args:
            base_url (str, optional): The API base URL. Defaults to the development server.
            api_key (str, optional): Your API key. If omitted, only public endpoints work.
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Configure Retries (Reliability)
        retry_strategy = Retry(
            total=3,
            backoff_factor=1, # 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PATCH", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Set up authentication header if API key is provided
        if api_key:
            self.session.headers['Authorization'] = f'Token {api_key}'
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
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
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError("Could not connect to the Eventyay API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError("The request to the Eventyay API timed out.")
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")
    
    def _post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs a POST request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint path.
            json (dict, optional): The JSON payload for the request.

        Returns:
            Dict[str, Any]: The parsed JSON response data.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError("Could not connect to the Eventyay API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError("The request to the Eventyay API timed out.")
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")

    def _patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs a PATCH request to a specified endpoint.

        Args:
            endpoint (str): The API endpoint path.
            json (dict, optional): The JSON payload (partial update).

        Returns:
            Dict[str, Any]: The parsed JSON response data.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.patch(url, json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError("Could not connect to the Eventyay API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError("The request to the Eventyay API timed out.")
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
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.delete(url)
            # 204 No Content is common for delete
            if response.status_code == 204:
                return
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e.response)
        except requests.exceptions.ConnectionError:
            raise EventyayConnectionError("Could not connect to the Eventyay API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise EventyayTimeoutError("The request to the Eventyay API timed out.")
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")
    
    def _handle_error(self, response: requests.Response) -> None:
        """
        Maps HTTP error responses to SDK-specific exceptions.
        
        Args:
            response (requests.Response): The failing response object.
        """
        status_code = response.status_code
        
        try:
            error_data = response.json()
            error_message = error_data.get('detail') or error_data.get('message') or str(error_data)
        except ValueError:
            error_message = response.text or f"HTTP {status_code} error"
        
        if status_code == 401 or status_code == 403:
            raise EventyayAuthenticationError(error_message)
        if status_code == 404:
            raise EventyayNotFoundError(error_message)
            
        if status_code == 429:
            raise EventyayRateLimitError(f"Rate limit exceeded. Try again later. {error_message}")
            
        if 400 <= status_code < 500:
            raise EventyayValidationError(error_message)
        else:
            raise EventyayAPIError(f"HTTP {status_code}: {error_message}")
