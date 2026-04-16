from typing import Any, Dict, Optional

from ._transport import AsyncTransportBase
from .models import (
    AccessCode,
    AccessCodeList,
    Attendee,
    AttendeeList,
    DiscountCode,
    DiscountCodeList,
    Event,
    EventList,
    EventSubTopic,
    EventSubTopicList,
    EventTopic,
    EventTopicList,
    EventType,
    EventTypeList,
    Feedback,
    FeedbackList,
    Microlocation,
    MicrolocationList,
    GenericResource,
    GenericResourceList,
    Notification,
    NotificationList,
    Order,
    OrderList,
    Organizer,
    OrganizerList,
    Page,
    PageList,
    Role,
    RoleInvite,
    RoleInviteList,
    RoleList,
    Session,
    SessionList,
    Service,
    ServiceList,
    Setting,
    SettingList,
    Speaker,
    SpeakerList,
    Sponsor,
    SponsorList,
    Tax,
    Ticket,
    TicketTag,
    TicketTagList,
    TicketList,
    Track,
    TrackList,
    User,
    UserList,
)
from .utils import build_jsonapi_payload, parse_jsonapi_list, parse_jsonapi_resource


class AsyncOrganizersMixin(AsyncTransportBase):
    """Async methods for Organizers."""

    async def get_organizers(self) -> OrganizerList:
        """
        Fetch all organizers (Async).

        Returns:
            OrganizerList object.
        """
        response_data = await self._get("organizers")
        return OrganizerList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_organizer(self, organizer_id: str) -> Organizer:
        """
        Get details of a specific organizer (Async).

        Args:
            organizer_id: The ID of the organizer.

        Returns:
            Organizer object.
        """
        response_data = await self._get(f"organizers/{organizer_id}")
        return Organizer(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_organizer_events(self, organizer_id: str, page: int = 1) -> EventList:
        """
        Get all events for a specific organizer (Async).

        Args:
            organizer_id: The ID of the organizer.
            page: Page number (default: 1).

        Returns:
            EventList object containing events and pagination info.
        """
        params = {"page[number]": page}
        response_data = await self._get(f"organizers/{organizer_id}/events", params=params)
        return EventList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def create_organizer(
        self,
        name: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        logo_url: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Organizer:
        """
        Create a new organizer (Async).

        Args:
            name: Name of the organizer (Required).
            description: Description of the organizer.
            url: Website URL.
            logo_url: Logo URL.

        Returns:
            Created Organizer object.
        """
        data = {"name": name}
        if description:
            data["description"] = description
        if url:
            data["url"] = url
        if logo_url:
            data["logo_url"] = logo_url

        payload = build_jsonapi_payload("organizer", data)
        response_data = await self._post(
            "organizers",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return Organizer(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def update_organizer(
        self,
        organizer_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        logo_url: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Organizer:
        """
        Update an existing organizer (Async).

        Args:
            organizer_id: The ID of the organizer to update.
            name: New name.
            description: New description.
            url: New website URL.
            logo_url: New logo URL.

        Returns:
            Updated Organizer object.
        """
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if url:
            data["url"] = url
        if logo_url:
            data["logo_url"] = logo_url

        if not data:
            return await self.get_organizer(organizer_id)

        payload = build_jsonapi_payload("organizer", data, resource_id=str(organizer_id))
        response_data = await self._patch(
            f"organizers/{organizer_id}",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return Organizer(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def delete_organizer(self, organizer_id: str) -> bool:
        """
        Delete an organizer (Async).

        Args:
            organizer_id: The ID of the organizer to delete.

        Returns:
            True if deletion was successful.
        """
        await self._delete(f"organizers/{organizer_id}")
        return True


class AsyncEventsMixin(AsyncTransportBase):
    """Async methods for Events."""

    async def get_events(self) -> EventList:
        """
        Fetch all public events (Async).

        Returns:
            EventList object.
        """
        response_data = await self._get("events")
        return EventList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_tax(self, event_id: str) -> Tax:
        """
        Get tax details for a specific event (Async).

        Args:
            event_id: The ID of the event to retrieve tax information for.

        Returns:
            Tax object.
        """
        response_data = await self._get(f"events/{event_id}/tax")
        return Tax(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_event(self, event_id: int) -> Event:
        """
        Get a single event by ID (Async).

        Args:
            event_id: The ID of the event to retrieve.

        Returns:
            Event object.
        """
        response_data = await self._get(f"events/{event_id}")
        return Event(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_event_speakers(self, event_id: str) -> SpeakerList:
        """
        Get all speakers for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            SpeakerList object.
        """
        response_data = await self._get(f"events/{event_id}/speakers")
        return SpeakerList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_event_sessions(self, event_id: str) -> SessionList:
        """
        Get all sessions (talks) for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            SessionList object.
        """
        response_data = await self._get(f"events/{event_id}/sessions")
        return SessionList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def create_event(
        self,
        name: str,
        identifier: str,
        starts_at: str,
        ends_at: str,
        timezone: str,
        privacy: str = "public",
        location_name: Optional[str] = None,
        online: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> Event:
        """
        Create a new event (Async).

        Args:
            name: Event name.
            identifier: Unique identifier (slug).
            starts_at: Start time (ISO 8601).
            ends_at: End time (ISO 8601).
            timezone: Timezone string (e.g. 'UTC').
            privacy: 'public' or 'private'.
            location_name: Name of the location.
            online: Whether the event is online.

        Returns:
            Created Event object.
        """
        data = {
            "name": name,
            "identifier": identifier,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "timezone": timezone,
            "privacy": privacy,
            "online": online,
        }
        if location_name:
            data["location_name"] = location_name

        payload = build_jsonapi_payload("event", data)
        response_data = await self._post(
            "events",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return Event(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def update_event(
        self,
        event_id: int,
        name: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        timezone: Optional[str] = None,
        privacy: Optional[str] = None,
        location_name: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Event:
        """
        Update an existing event (Async).

        Args:
            event_id: The ID of the event.
            name: New name.
            starts_at: New start time.
            ends_at: New end time.
            timezone: New timezone.
            privacy: New privacy setting.
            location_name: New location name.

        Returns:
            Updated Event object.
        """
        data = {}
        if name:
            data["name"] = name
        if starts_at:
            data["starts_at"] = starts_at
        if ends_at:
            data["ends_at"] = ends_at
        if timezone:
            data["timezone"] = timezone
        if privacy:
            data["privacy"] = privacy
        if location_name:
            data["location_name"] = location_name

        if not data:
            return await self.get_event(event_id)

        payload = build_jsonapi_payload("event", data, resource_id=str(event_id))
        response_data = await self._patch(
            f"events/{event_id}",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return Event(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def delete_event(self, event_id: int) -> bool:
        """
        Delete an event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            True if successful.
        """
        await self._delete(f"events/{event_id}")
        return True


class AsyncEventTypesMixin(AsyncTransportBase):
    """Async methods for Event Types."""

    async def get_event_types(self, page: int = 1, page_size: int = 10) -> EventTypeList:
        """Retrieve paginated event types (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("event-types", params=params)
        return EventTypeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_event_type(self, event_type_id: str) -> EventType:
        """Get a single event type by ID (Async)."""
        response_data = await self._get(f"event-types/{event_type_id}")
        return EventType(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncEventTopicsMixin(AsyncTransportBase):
    """Async methods for Event Topics."""

    async def get_event_topics(self, page: int = 1, page_size: int = 10) -> EventTopicList:
        """Retrieve paginated event topics (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("event-topics", params=params)
        return EventTopicList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_event_topic(self, event_topic_id: str) -> EventTopic:
        """Get a single event topic by ID (Async)."""
        response_data = await self._get(f"event-topics/{event_topic_id}")
        return EventTopic(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncEventSubTopicsMixin(AsyncTransportBase):
    """Async methods for Event Sub Topics."""

    async def get_event_sub_topics(self, page: int = 1, page_size: int = 10) -> EventSubTopicList:
        """Retrieve paginated event sub topics (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("event-sub-topics", params=params)
        return EventSubTopicList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_event_sub_topic(self, event_sub_topic_id: str) -> EventSubTopic:
        """Get a single event sub topic by ID (Async)."""
        response_data = await self._get(f"event-sub-topics/{event_sub_topic_id}")
        return EventSubTopic(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncTicketsMixin(AsyncTransportBase):
    """Async methods for Tickets."""

    async def get_event_tickets(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> TicketList:
        """
        Retrieves a paginated list of tickets for a specific event (Async).

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of tickets per page. Defaults to 10.

        Returns:
            TicketList: A Pydantic model containing the list of tickets and pagination metadata.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/tickets", params=params)
        return TicketList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_ticket(self, event_identifier: str, ticket_id: str) -> Ticket:
        """
        Fetches details for a single specific ticket (Async).

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            ticket_id (str): The unique identifier of the ticket.

        Returns:
            Ticket: The detailed Ticket object.

        Raises:
            EventyayNotFoundError: If no ticket is found with the given ID.
        """
        response_data = await self._get(f"events/{event_identifier}/tickets/{ticket_id}")
        return Ticket(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncAttendeesMixin(AsyncTransportBase):
    """Async methods for Attendees."""

    async def get_event_attendees(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> AttendeeList:
        """
        Retrieves a paginated list of attendees for a specific event (Async).

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of attendees per page. Defaults to 10.

        Returns:
            AttendeeList: A Pydantic model containing the list of attendees and pagination metadata.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/attendees", params=params)
        return AttendeeList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_attendee(self, event_identifier: str, attendee_id: str) -> Attendee:
        """
        Fetches details for a single specific attendee (Async).

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            attendee_id (str): The unique identifier of the attendee.

        Returns:
            Attendee: The detailed Attendee object.
        """
        response_data = await self._get(f"events/{event_identifier}/attendees/{attendee_id}")
        return Attendee(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncSpeakersMixin(AsyncTransportBase):
    """Async methods for standalone Speakers."""

    async def get_speaker(self, event_identifier: str, speaker_id: str) -> Speaker:
        """
        Fetches details for a single specific speaker asynchronously.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            speaker_id (str): The unique identifier of the speaker.

        Returns:
            Speaker: The detailed Speaker object.
        """
        response_data = await self._get(f"events/{event_identifier}/speakers/{speaker_id}")
        return Speaker(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncSessionsMixin(AsyncTransportBase):
    """Async methods for standalone Sessions."""

    async def get_session(self, event_identifier: str, session_id: str) -> Session:
        """
        Fetches details for a single specific session asynchronously.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            session_id (str): The unique identifier of the session.

        Returns:
            Session: The detailed Session object.
        """
        response_data = await self._get(f"events/{event_identifier}/sessions/{session_id}")
        return Session(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncTracksMixin(AsyncTransportBase):
    """Async methods for Tracks."""

    async def get_event_tracks(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> TrackList:
        """Retrieves paginated tracks for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/tracks", params=params)
        return TrackList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_track(self, event_identifier: str, track_id: str) -> Track:
        """Fetches a single track (Async)."""
        response_data = await self._get(f"events/{event_identifier}/tracks/{track_id}")
        return Track(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncMicrolocationsMixin(AsyncTransportBase):
    """Async methods for Microlocations."""

    async def get_event_microlocations(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> MicrolocationList:
        """Retrieves paginated microlocations for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/microlocations", params=params)
        return MicrolocationList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_microlocation(
        self, event_identifier: str, microlocation_id: str
    ) -> Microlocation:
        """Fetches a single microlocation (Async)."""
        response_data = await self._get(
            f"events/{event_identifier}/microlocations/{microlocation_id}"
        )
        return Microlocation(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncSponsorsMixin(AsyncTransportBase):
    """Async methods for Sponsors."""

    async def get_event_sponsors(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> SponsorList:
        """Retrieves paginated sponsors for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/sponsors", params=params)
        return SponsorList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_sponsor(self, event_identifier: str, sponsor_id: str) -> Sponsor:
        """Fetches a single sponsor (Async)."""
        response_data = await self._get(f"events/{event_identifier}/sponsors/{sponsor_id}")
        return Sponsor(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncDiscountCodesMixin(AsyncTransportBase):
    """Async methods for Discount Codes."""

    async def get_event_discount_codes(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> DiscountCodeList:
        """Retrieves paginated discount codes for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/discount-codes", params=params)
        return DiscountCodeList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_discount_code(self, event_identifier: str, code_id: str) -> DiscountCode:
        """Fetches a single discount code (Async)."""
        response_data = await self._get(f"events/{event_identifier}/discount-codes/{code_id}")
        return DiscountCode(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncAccessCodesMixin(AsyncTransportBase):
    """Async methods for Access Codes."""

    async def get_event_access_codes(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> AccessCodeList:
        """Retrieve event access codes (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/access-codes", params=params)
        return AccessCodeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_ticket_access_codes(
        self, ticket_id: str, page: int = 1, page_size: int = 10
    ) -> AccessCodeList:
        """Retrieve ticket access codes (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"tickets/{ticket_id}/access-codes", params=params)
        return AccessCodeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_user_access_codes(
        self, user_id: str, page: int = 1, page_size: int = 10
    ) -> AccessCodeList:
        """Retrieve user access codes (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"users/{user_id}/access-codes", params=params)
        return AccessCodeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_access_code(self, access_code_id: str) -> AccessCode:
        """Get a single access code by ID (Async)."""
        response_data = await self._get(f"access-codes/{access_code_id}")
        return AccessCode(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncNotificationsMixin(AsyncTransportBase):
    """Async methods for Notifications."""

    async def get_notifications(self, page: int = 1, page_size: int = 25) -> NotificationList:
        """Retrieve paginated notifications (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("notifications", params=params)
        return NotificationList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_notification(self, notification_id: str) -> Notification:
        """Get a single notification by ID (Async)."""
        response_data = await self._get(f"notifications/{notification_id}")
        return Notification(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncPagesMixin(AsyncTransportBase):
    """Async methods for Pages."""

    async def get_pages(self, page: int = 1, page_size: int = 25) -> PageList:
        """Retrieve paginated pages (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("pages", params=params)
        return PageList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_page(self, page_id: str) -> Page:
        """Get a single page by ID (Async)."""
        response_data = await self._get(f"pages/{page_id}")
        return Page(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncServicesMixin(AsyncTransportBase):
    """Async methods for Services."""

    async def get_services(self, page: int = 1, page_size: int = 25) -> ServiceList:
        """Retrieve paginated services (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("services", params=params)
        return ServiceList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_service(self, service_id: str) -> Service:
        """Get a single service by ID (Async)."""
        response_data = await self._get(f"services/{service_id}")
        return Service(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_access_code_by_code(self, code: str) -> AccessCode:
        """Get access code details by code value (Async)."""
        response_data = await self._get(f"access-codes/{code}")
        return AccessCode(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )


class AsyncOrdersMixin(AsyncTransportBase):
    """Async methods for Orders."""

    async def get_event_orders(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> OrderList:
        """Retrieves paginated orders for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/orders", params=params)
        return OrderList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_order(self, event_identifier: str, order_identifier: str) -> Order:
        """Fetches a single order (Async)."""
        response_data = await self._get(f"events/{event_identifier}/orders/{order_identifier}")
        return Order(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncTaxMixin(AsyncTransportBase):
    """Async methods for Tax."""

    async def get_event_tax(self, event_identifier: str) -> Tax:
        """Retrieves the tax configuration for an event (Async)."""
        response_data = await self._get(f"events/{event_identifier}/tax")
        return Tax(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncUsersMixin(AsyncTransportBase):
    """Async methods for Users."""

    async def get_users(self, page: int = 1, page_size: int = 25) -> UserList:
        """
        Fetch all users (Async). Requires Admin.

        Returns:
            UserList object.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("users", params=params)
        return UserList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_user(self, user_id: str) -> User:
        """
        Get details of a specific user (Async).

        Args:
            user_id: The ID of the user.

        Returns:
            User object.
        """
        response_data = await self._get(f"users/{user_id}")
        return User(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def update_user(
        self,
        user_id: str,
        payload: Dict[str, Any],
        idempotency_key: Optional[str] = None,
    ) -> User:
        """
        Update an existing user (Async).

        Args:
            user_id: The ID of the user.
            payload: JSON patch payload.

        Returns:
            Updated User object.
        """
        payload_wrap = build_jsonapi_payload("user", payload, resource_id=str(user_id))
        response_data = await self._patch(
            f"users/{user_id}",
            json=payload_wrap,
            idempotency_key=idempotency_key,
        )
        return User(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncRolesMixin(AsyncTransportBase):
    """Async methods for Roles."""

    async def get_event_roles(self, event_id: str, page: int = 1, page_size: int = 25) -> RoleList:
        """Fetch roles for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_id}/roles", params=params)
        return RoleList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_role(self, event_id: str, role_id: str) -> Role:
        """Get a single role (Async)."""
        response_data = await self._get(f"events/{event_id}/roles/{role_id}")
        return Role(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncRoleInvitesMixin(AsyncTransportBase):
    """Async methods for Role Invites."""

    async def get_role_invites(self, page: int = 1, page_size: int = 25) -> RoleInviteList:
        """Fetch paginated role invites (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get("role-invites", params=params)
        return RoleInviteList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_role_invite(self, invite_id: str) -> RoleInvite:
        """Fetch a single role invite (Async)."""
        response_data = await self._get(f"role-invites/{invite_id}")
        return RoleInvite(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def create_role_invite(
        self,
        email: str,
        role_id: str,
        event_id: str,
        idempotency_key: Optional[str] = None,
    ) -> RoleInvite:
        """Create a role invite (Async)."""
        payload = build_jsonapi_payload(
            "role-invite",
            {"email": email, "role_id": role_id, "event_id": event_id},
        )
        response_data = await self._post(
            "role-invites",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return RoleInvite(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def delete_role_invite(self, invite_id: str) -> bool:
        """Delete a role invite (Async)."""
        await self._delete(f"role-invites/{invite_id}")
        return True


class AsyncFeedbacksMixin(AsyncTransportBase):
    """Async methods for Feedbacks."""

    async def get_event_feedbacks(
        self, event_id: str, page: int = 1, page_size: int = 25
    ) -> FeedbackList:
        """Fetch feedbacks for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_id}/feedbacks", params=params)
        return FeedbackList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_feedback(self, event_id: str, feedback_id: str) -> Feedback:
        """Get a single feedback entry (Async)."""
        response_data = await self._get(f"events/{event_id}/feedbacks/{feedback_id}")
        return Feedback(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncSettingsMixin(AsyncTransportBase):
    """Async methods for Settings."""

    async def get_settings(
        self, page: Optional[int] = None, page_size: Optional[int] = None, **kwargs: Any
    ) -> SettingList:
        """
        Get a paginated list of global settings (Async).

        Args:
            page (Optional[int]): The page number to retrieve. Defaults to None.
            page_size (Optional[int]): The number of items per page. Defaults to None.
            **kwargs: Additional query parameters (e.g., filter, sort).

        Returns:
            SettingList: A paginated list of settings.
        """
        params = kwargs.copy()
        if page is not None:
            params["page[number]"] = page
        if page_size is not None:
            params["page[size]"] = page_size

        response_data = await self._get("settings", params=params)
        return SettingList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    async def get_setting(self, setting_id: str, **kwargs: Any) -> Setting:
        """
        Get a specific setting by ID (Async).

        Args:
            setting_id (str): The ID of the setting.
            **kwargs: Additional query parameters.

        Returns:
            Setting: The setting details.
        """
        response_data = await self._get(f"settings/{setting_id}", params=kwargs)
        return Setting(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))


class AsyncTicketTagsMixin(AsyncTransportBase):
    """Async methods for Ticket Tags."""

    async def get_event_ticket_tags(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> TicketTagList:
        """Retrieve ticket tags for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"events/{event_identifier}/ticket-tags", params=params)
        return TicketTagList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_ticket_ticket_tags(
        self, ticket_id: str, page: int = 1, page_size: int = 10
    ) -> TicketTagList:
        """Retrieve ticket tags for a ticket (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(f"tickets/{ticket_id}/ticket-tags", params=params)
        return TicketTagList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_ticket_tag(self, tag_id: str) -> TicketTag:
        """Get a single ticket tag (Async)."""
        response_data = await self._get(f"ticket-tags/{tag_id}")
        return TicketTag(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def create_ticket_tag(
        self,
        name: str,
        color: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> TicketTag:
        """Create a ticket tag (Async)."""
        attributes = {"name": name}
        if color is not None:
            attributes["color"] = color

        payload = build_jsonapi_payload("ticket-tag", attributes)
        response_data = await self._post(
            "ticket-tags",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return TicketTag(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def update_ticket_tag(
        self,
        tag_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> TicketTag:
        """Update a ticket tag (Async)."""
        attributes = {}
        if name is not None:
            attributes["name"] = name
        if color is not None:
            attributes["color"] = color

        if not attributes:
            return await self.get_ticket_tag(tag_id)

        payload = build_jsonapi_payload("ticket-tag", attributes, resource_id=str(tag_id))
        response_data = await self._patch(
            f"ticket-tags/{tag_id}",
            json=payload,
            idempotency_key=idempotency_key,
        )
        return TicketTag(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def delete_ticket_tag(self, tag_id: str) -> bool:
        """Delete a ticket tag (Async)."""
        await self._delete(f"ticket-tags/{tag_id}")
        return True


class AsyncMiscResourcesMixin(AsyncTransportBase):
    """Async broad read/list coverage for additional Eventyay API domains."""

    async def _list_generic(self, endpoint: str, page: int = 1, page_size: int = 25) -> GenericResourceList:
        params = {"page[number]": page, "page[size]": page_size}
        response_data = await self._get(endpoint, params=params)
        return GenericResourceList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def _get_generic(self, endpoint: str) -> GenericResource:
        response_data = await self._get(endpoint)
        return GenericResource(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    async def get_activities(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("activities", page, page_size)

    async def get_activity(self, activity_id: str) -> GenericResource:
        return await self._get_generic(f"activities/{activity_id}")

    async def get_event_locations(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("event-locations", page, page_size)

    async def get_event_location(self, event_location_id: str) -> GenericResource:
        return await self._get_generic(f"event-locations/{event_location_id}")

    async def get_invoices(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("event-invoices", page, page_size)

    async def get_invoice(self, invoice_id: str) -> GenericResource:
        return await self._get_generic(f"event-invoices/{invoice_id}")

    async def get_mails(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("mails", page, page_size)

    async def get_mail(self, mail_id: str) -> GenericResource:
        return await self._get_generic(f"mails/{mail_id}")

    async def get_message_settings(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("message-settings", page, page_size)

    async def get_message_setting(self, message_setting_id: str) -> GenericResource:
        return await self._get_generic(f"message-settings/{message_setting_id}")

    async def get_import_jobs(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("import-jobs", page, page_size)

    async def get_import_job(self, import_job_id: str) -> GenericResource:
        return await self._get_generic(f"import-jobs/{import_job_id}")

    async def get_video_streams(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("video-streams", page, page_size)

    async def get_video_stream(self, video_stream_id: str) -> GenericResource:
        return await self._get_generic(f"video-streams/{video_stream_id}")

    async def get_user_permissions(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("user-permissions", page, page_size)

    async def get_user_permission(self, user_permission_id: str) -> GenericResource:
        return await self._get_generic(f"user-permissions/{user_permission_id}")

    async def get_ticket_fees(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("ticket-fees", page, page_size)

    async def get_ticket_fee(self, ticket_fee_id: str) -> GenericResource:
        return await self._get_generic(f"ticket-fees/{ticket_fee_id}")

    async def get_custom_placeholders(
        self, page: int = 1, page_size: int = 25
    ) -> GenericResourceList:
        return await self._list_generic("custom-placeholders", page, page_size)

    async def get_custom_placeholder(self, custom_placeholder_id: str) -> GenericResource:
        return await self._get_generic(f"custom-placeholders/{custom_placeholder_id}")

    async def get_groups(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("groups", page, page_size)

    async def get_group(self, group_id: str) -> GenericResource:
        return await self._get_generic(f"groups/{group_id}")

    async def get_panel_permissions(self, page: int = 1, page_size: int = 25) -> GenericResourceList:
        return await self._list_generic("panel-permissions", page, page_size)

    async def get_panel_permission(self, panel_permission_id: str) -> GenericResource:
        return await self._get_generic(f"panel-permissions/{panel_permission_id}")

    async def get_custom_system_roles(
        self, page: int = 1, page_size: int = 25
    ) -> GenericResourceList:
        return await self._list_generic("custom-system-roles", page, page_size)

    async def get_custom_system_role(self, custom_system_role_id: str) -> GenericResource:
        return await self._get_generic(f"custom-system-roles/{custom_system_role_id}")

    async def get_event_role_permissions(
        self, page: int = 1, page_size: int = 25
    ) -> GenericResourceList:
        return await self._list_generic("event-role-permissions", page, page_size)

    async def get_event_role_permission(self, event_role_permission_id: str) -> GenericResource:
        return await self._get_generic(f"event-role-permissions/{event_role_permission_id}")

    async def get_email_notifications(
        self, page: int = 1, page_size: int = 25
    ) -> GenericResourceList:
        return await self._list_generic("email-notifications", page, page_size)

    async def get_email_notification(self, email_notification_id: str) -> GenericResource:
        return await self._get_generic(f"email-notifications/{email_notification_id}")


class AsyncAuthMixin(AsyncTransportBase):
    """Async authentication and account-security operations."""

    async def login(self, email: str, password: str, remember_me: bool = False) -> Dict[str, Any]:
        payload = {"email": email, "password": password, "remember_me": remember_me}
        return await self._post("auth/login", json=payload)

    async def logout(self, refresh_token: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if refresh_token is not None:
            payload["refresh_token"] = refresh_token
        return await self._post("auth/logout", json=payload)

    async def verify_password(self, password: str) -> Dict[str, Any]:
        return await self._post("auth/verify-password", json={"password": password})

    async def change_password(self, old_password: str, new_password: str) -> Dict[str, Any]:
        payload = {"old_password": old_password, "new_password": new_password}
        return await self._post("auth/change-password", json=payload)

    async def request_password_reset(self, email: str) -> Dict[str, Any]:
        return await self._post("auth/reset-password", json={"email": email})

    async def reset_password_with_token(self, token: str, new_password: str) -> Dict[str, Any]:
        payload = {"token": token, "password": new_password}
        return await self._patch("auth/reset-password", json=payload)

    async def resend_email_verification(self, email: str) -> Dict[str, Any]:
        return await self._post("auth/resend-verification-email", json={"email": email})

    async def verify_email(self, token: str) -> Dict[str, Any]:
        return await self._post("auth/verify-email", json={"token": token})


class AsyncOperationsMixin(AsyncTransportBase):
    """Async operational endpoints for copy/upload-image workflows."""

    async def copy_event(self, event_id: str) -> Dict[str, Any]:
        return await self._post(f"events/{event_id}/copy")

    async def upload_image(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("upload/image", json=payload)
