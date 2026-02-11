"""
Eventyay API Client

Main client class for interacting with the Eventyay REST API.
"""

import requests
from typing import Optional, Dict, Any
from .exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayNotFoundError,
    EventyayValidationError
)


from .organizers import OrganizersMixin
from .events import EventsMixin

class EventyayClient(OrganizersMixin, EventsMixin):
    """
    Main client for the Eventyay API.
    
    Args:
        base_url: The base URL for the Eventyay API (default: https://dev.eventyay.com/api/v1)
        api_key: Optional API key for authentication
    
    Example:
        >>> client = EventyayClient()
        >>> organizers = client.get_organizers()
        
        With authentication:
        >>> client = EventyayClient(api_key="your-api-key")
    """
    
    def __init__(
        self,
        base_url: str = "https://dev.eventyay.com/api/v1",
        api_key: Optional[str] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
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
        Make a GET request to the API.
        
        Args:
            endpoint: The API endpoint (without base URL)
            params: Optional query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            EventyayAPIError: For general API errors
            EventyayAuthenticationError: For authentication failures
            EventyayNotFoundError: For 404 errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(response)
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")
    
    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(response)
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")
    
    def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(response)
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")
    
    def _delete(self, endpoint: str) -> None:
        """Make a DELETE request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.delete(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._handle_error(response)
        except requests.exceptions.RequestException as e:
            raise EventyayAPIError(f"Request failed: {str(e)}")
    
    def _handle_error(self, response: requests.Response) -> None:
        """
        Handle HTTP errors and raise appropriate exceptions.
        
        Args:
            response: The failed response object
        """
        status_code = response.status_code
        
        try:
            error_data = response.json()
            error_message = error_data.get('detail') or error_data.get('message') or str(error_data)
        except ValueError:
            error_message = response.text or f"HTTP {status_code} error"
        
        if status_code == 401 or status_code == 403:
            raise EventyayAuthenticationError(error_message)
        elif status_code == 404:
            raise EventyayNotFoundError(error_message)
        elif status_code == 400:
            raise EventyayValidationError(error_message)
        else:
            raise EventyayAPIError(f"HTTP {status_code}: {error_message}")
