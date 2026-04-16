from typing import Optional

from ._transport import SyncTransportBase
from .models import TicketTag, TicketTagList
from .utils import build_jsonapi_payload, parse_jsonapi_list, parse_jsonapi_resource


class TicketTagsMixin(SyncTransportBase):
    """Mixin class for interacting with Ticket Tag endpoints."""

    def get_event_ticket_tags(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> TicketTagList:
        """Retrieve ticket tags for an event."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_identifier}/ticket-tags", params=params)
        return TicketTagList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_ticket_ticket_tags(
        self, ticket_id: str, page: int = 1, page_size: int = 10
    ) -> TicketTagList:
        """Retrieve ticket tags linked to a ticket."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"tickets/{ticket_id}/ticket-tags", params=params)
        return TicketTagList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_ticket_tag(self, tag_id: str) -> TicketTag:
        """Fetch a single ticket tag by ID."""
        response_data = self._get(f"ticket-tags/{tag_id}")
        return TicketTag(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def create_ticket_tag(
        self,
        name: str,
        color: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> TicketTag:
        """Create a ticket tag."""
        attributes = {"name": name}
        if color is not None:
            attributes["color"] = color

        payload = build_jsonapi_payload("ticket-tag", attributes)
        response_data = self._post("ticket-tags", json=payload, idempotency_key=idempotency_key)
        return TicketTag(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def update_ticket_tag(
        self,
        tag_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> TicketTag:
        """Update a ticket tag."""
        attributes = {}
        if name is not None:
            attributes["name"] = name
        if color is not None:
            attributes["color"] = color

        if not attributes:
            return self.get_ticket_tag(tag_id)

        payload = build_jsonapi_payload("ticket-tag", attributes, resource_id=str(tag_id))
        response_data = self._patch(
            f"ticket-tags/{tag_id}",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return TicketTag(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def delete_ticket_tag(self, tag_id: str) -> bool:
        """Delete a ticket tag by ID."""
        self._delete(f"ticket-tags/{tag_id}")
        return True
