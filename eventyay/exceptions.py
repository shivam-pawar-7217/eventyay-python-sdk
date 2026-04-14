"""
Eventyay API Exceptions

Custom exception classes for the Eventyay SDK.
Each exception carries the HTTP status code and response body (when available)
so that callers can inspect failures programmatically.
"""

from typing import Optional


class EventyayAPIError(Exception):
    """Base exception for all Eventyay API errors.

    Attributes:
        message (str): Human-readable error description.
        status_code (Optional[int]): The HTTP status code, if available.
        response_body (Optional[str]): The raw response body, if available.
    """

    def __init__(
        self,
        message: str = "An API error occurred",
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)

    def __str__(self):
        parts = [self.message]
        if self.status_code:
            parts.insert(0, f"[HTTP {self.status_code}]")
        return " ".join(parts)


class EventyayAuthenticationError(EventyayAPIError):
    """Raised when authentication fails (401/403 errors)."""


class EventyayNotFoundError(EventyayAPIError):
    """Raised when a resource is not found (404 errors)."""


class EventyayValidationError(EventyayAPIError):
    """Raised when request validation fails (400 errors)."""


class EventyayConnectionError(EventyayAPIError):
    """Raised when a network connection error occurs."""


class EventyayTimeoutError(EventyayAPIError):
    """Raised when a request times out."""


class EventyayRateLimitError(EventyayAPIError):
    """Raised when the API rate limit is exceeded (HTTP 429)."""
