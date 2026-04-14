"""
Eventyay API Exceptions

Custom exception classes for the Eventyay SDK.
Each exception carries the HTTP status code and response body (when available)
so that callers can inspect failures programmatically.
"""

import re
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
        self.response_body = self._sanitize_response_body(response_body)
        super().__init__(self.message)

    @staticmethod
    def _sanitize_response_body(response_body: Optional[str], limit: int = 2048) -> Optional[str]:
        """Reduce accidental leakage by truncating and redacting common credential patterns."""
        if response_body is None:
            return None

        body = response_body[:limit]

        # Redact auth-like key/value entries in JSON-ish or plain text content.
        body = re.sub(
            r'(?i)("?(token|access_token|refresh_token|api_key|apikey)"?\s*[:=]\s*"?)[^"\s,}]+',
            r"\1[REDACTED]",
            body,
        )

        # Redact bearer/jwt style header values.
        body = re.sub(
            r"(?i)(authorization\s*:\s*(bearer|jwt|token)\s+)[^\s,]+",
            r"\1[REDACTED]",
            body,
        )

        return body

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
