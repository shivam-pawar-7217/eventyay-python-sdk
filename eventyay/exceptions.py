"""
Eventyay API Exceptions

Custom exception classes for the Eventyay SDK.
"""


class EventyayAPIError(Exception):
    """Base exception for all Eventyay API errors."""
    pass


class EventyayAuthenticationError(EventyayAPIError):
    """Raised when authentication fails (401/403 errors)."""
    pass


class EventyayNotFoundError(EventyayAPIError):
    """Raised when a resource is not found (404 errors)."""
    pass


class EventyayValidationError(EventyayAPIError):
    """Raised when request validation fails (400 errors)."""
    pass
