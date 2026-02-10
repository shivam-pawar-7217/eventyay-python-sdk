"""
Eventyay Python SDK

A Python client library for the Eventyay API.
"""

__version__ = "0.1.0"
__author__ = "Shivam Pawar"
__email__ = "shivam.pawar.7217@example.com"

from .client import EventyayClient
from .exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayNotFoundError,
    EventyayValidationError
)

__all__ = [
    "EventyayClient",
    "EventyayAPIError",
    "EventyayAuthenticationError",
    "EventyayNotFoundError",
    "EventyayValidationError",
]
