"""
Eventyay Python SDK

A modern, type-safe Python client library for the Eventyay API.
Supports both synchronous and asynchronous usage with Pydantic models.
"""

__version__ = "0.1.0"
__author__ = "Shivam Pawar"
__email__ = "shivam.pawar.7217@example.com"

from .async_client import AsyncEventyayClient
from .client import EventyayClient
from .exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayConnectionError,
    EventyayNotFoundError,
    EventyayRateLimitError,
    EventyayTimeoutError,
    EventyayValidationError,
)
from .models import (
    Attendee,
    AttendeeList,
    DiscountCode,
    DiscountCodeList,
    Event,
    EventList,
    Feedback,
    FeedbackList,
    Microlocation,
    MicrolocationList,
    Order,
    OrderList,
    Organizer,
    OrganizerList,
    Role,
    RoleList,
    Session,
    SessionList,
    Setting,
    SettingList,
    Speaker,
    SpeakerList,
    Sponsor,
    SponsorList,
    Tax,
    TaxList,
    Ticket,
    TicketList,
    Track,
    TrackList,
    User,
    UserList,
)

__all__ = [
    # Clients
    "EventyayClient",
    "AsyncEventyayClient",
    # Exceptions
    "EventyayAPIError",
    "EventyayAuthenticationError",
    "EventyayNotFoundError",
    "EventyayValidationError",
    "EventyayConnectionError",
    "EventyayTimeoutError",
    "EventyayRateLimitError",
    # Models
    "Organizer",
    "OrganizerList",
    "Event",
    "EventList",
    "Attendee",
    "AttendeeList",
    "Speaker",
    "SpeakerList",
    "Session",
    "SessionList",
    "Track",
    "TrackList",
    "Microlocation",
    "MicrolocationList",
    "Ticket",
    "TicketList",
    "Sponsor",
    "SponsorList",
    "DiscountCode",
    "DiscountCodeList",
    "Order",
    "OrderList",
    "Tax",
    "TaxList",
    "User",
    "UserList",
    "Role",
    "RoleList",
    "Feedback",
    "FeedbackList",
    "Setting",
    "SettingList",
]
