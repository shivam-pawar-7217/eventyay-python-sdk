from ._transport import SyncTransportBase
from .models import EventTopic, EventTopicList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class EventTopicsMixin(SyncTransportBase):
    """Mixin class for interacting with Event Topic endpoints."""

    def get_event_topics(self, page: int = 1, page_size: int = 10) -> EventTopicList:
        """Retrieve paginated event topics."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("event-topics", params=params)
        return EventTopicList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_event_topic(self, event_topic_id: str) -> EventTopic:
        """Fetch a single event topic by ID."""
        response_data = self._get(f"event-topics/{event_topic_id}")
        return EventTopic(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
