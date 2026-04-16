from ._transport import SyncTransportBase
from .models import EventSubTopic, EventSubTopicList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class EventSubTopicsMixin(SyncTransportBase):
    """Mixin class for interacting with Event Sub Topic endpoints."""

    def get_event_sub_topics(self, page: int = 1, page_size: int = 10) -> EventSubTopicList:
        """Retrieve paginated event sub topics."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("event-sub-topics", params=params)
        return EventSubTopicList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_event_sub_topic(self, event_sub_topic_id: str) -> EventSubTopic:
        """Fetch a single event sub topic by ID."""
        response_data = self._get(f"event-sub-topics/{event_sub_topic_id}")
        return EventSubTopic(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
