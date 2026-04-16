from ._transport import SyncTransportBase
from .models import EventType, EventTypeList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class EventTypesMixin(SyncTransportBase):
    """Mixin class for interacting with Event Type endpoints."""

    def get_event_types(self, page: int = 1, page_size: int = 10) -> EventTypeList:
        """Retrieve paginated event types."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("event-types", params=params)
        return EventTypeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_event_type(self, event_type_id: str) -> EventType:
        """Fetch a single event type by ID."""
        response_data = self._get(f"event-types/{event_type_id}")
        return EventType(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
