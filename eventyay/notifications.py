from ._transport import SyncTransportBase
from .models import Notification, NotificationList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class NotificationsMixin(SyncTransportBase):
    """Mixin class for interacting with Notification endpoints."""

    def get_notifications(self, page: int = 1, page_size: int = 25) -> NotificationList:
        """Retrieve paginated notifications."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("notifications", params=params)
        return NotificationList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_notification(self, notification_id: str) -> Notification:
        """Fetch a single notification by ID."""
        response_data = self._get(f"notifications/{notification_id}")
        return Notification(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
