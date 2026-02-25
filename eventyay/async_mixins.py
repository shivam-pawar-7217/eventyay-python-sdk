from typing import List, Dict, Any, Optional
from .models import (
    Organizer,
    OrganizerList,
    Event,
    EventList,
    Attendee,
    AttendeeList,
    Speaker,
    SpeakerList,
    Session,
    SessionList,
    Ticket,
    TicketList,
    Track,
    TrackList,
    Microlocation,
    MicrolocationList,
    Sponsor,
    SponsorList,
    DiscountCode,
    DiscountCodeList,
    Order,
    OrderList,
    Tax,
    User,
    UserList,
    Role,
    RoleList,
)


class AsyncOrganizersMixin:
    """Async methods for Organizers."""

    async def get_organizers(self) -> OrganizerList:
        """
        Fetch all organizers (Async).

        Returns:
            OrganizerList object.
        """
        response_data = await self._get("organizers")
        return OrganizerList(**response_data)

    async def get_organizer(self, organizer_id: str) -> Organizer:
        """
        Get details of a specific organizer (Async).

        Args:
            organizer_id: The ID of the organizer.

        Returns:
            Organizer object.
        """
        response_data = await self._get(f"organizers/{organizer_id}")
        return Organizer(**response_data)

    async def get_organizer_events(self, organizer_id: str, page: int = 1) -> EventList:
        """
        Get all events for a specific organizer (Async).

        Args:
            organizer_id: The ID of the organizer.
            page: Page number (default: 1).

        Returns:
            EventList object containing events and pagination info.
        """
        params = {"page": page}
        response_data = await self._get(
            f"organizers/{organizer_id}/events", params=params
        )
        return EventList(**response_data)

    async def create_organizer(
        self,
        name: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        logo_url: Optional[str] = None,
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

        response_data = await self._post("organizers", json=data)
        return Organizer(**response_data)

    async def update_organizer(
        self,
        organizer_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        logo_url: Optional[str] = None,
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

        response_data = await self._patch(f"organizers/{organizer_id}", json=data)
        return Organizer(**response_data)

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


class AsyncEventsMixin:
    """Async methods for Events."""

    async def get_events(self) -> EventList:
        """
        Fetch all public events (Async).

        Returns:
            EventList object.
        """
        response_data = await self._get("events")
        return EventList(**response_data)

    async def get_tax(self, event_id: str) -> Tax:
        """
        Get tax details for a specific event (Async).

        Args:
            event_id: The ID of the event to retrieve tax information for.

        Returns:
            Tax object.
        """
        response = await self._get(f"events/{event_id}/tax")
        return Tax(**response["data"])

    async def get_event(self, event_id: int) -> Event:
        """
        Get a single event by ID (Async).

        Args:
            event_id: The ID of the event to retrieve.

        Returns:
            Event object.
        """
        response_data = await self._get(f"events/{event_id}")
        return Event(**response_data)

    async def get_event_attendees(self, event_id: str) -> AttendeeList:
        """
        Get all attendees for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            AttendeeList object.
        """
        response_data = await self._get(f"events/{event_id}/attendees")
        return AttendeeList(**response_data)

    async def get_event_speakers(self, event_id: str) -> SpeakerList:
        """
        Get all speakers for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            SpeakerList object.
        """
        response_data = await self._get(f"events/{event_id}/speakers")
        return SpeakerList(**response_data)

    async def get_event_sessions(self, event_id: str) -> SessionList:
        """
        Get all sessions (talks) for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            SessionList object.
        """
        response_data = await self._get(f"events/{event_id}/sessions")
        return SessionList(**response_data)

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

        response_data = await self._post("events", json=data)
        return Event(**response_data)

    async def update_event(
        self,
        event_id: int,
        name: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        timezone: Optional[str] = None,
        privacy: Optional[str] = None,
        location_name: Optional[str] = None,
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

        response_data = await self._patch(f"events/{event_id}", json=data)
        return Event(**response_data)

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


class AsyncTicketsMixin:
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
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/tickets", params=params
        )
        return TicketList(**response_data)

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
        response_data = await self._get(
            f"events/{event_identifier}/tickets/{ticket_id}"
        )
        return Ticket(**response_data)


class AsyncAttendeesMixin:
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
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/attendees", params=params
        )
        return AttendeeList(**response_data)

    async def get_attendee(self, event_identifier: str, attendee_id: str) -> Attendee:
        """
        Fetches details for a single specific attendee (Async).

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            attendee_id (str): The unique identifier of the attendee.

        Returns:
            Attendee: The detailed Attendee object.
        """
        response_data = await self._get(
            f"events/{event_identifier}/attendees/{attendee_id}"
        )
        return Attendee(**response_data)


class AsyncSpeakersMixin:
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
        response_data = await self._get(
            f"events/{event_identifier}/speakers/{speaker_id}"
        )
        return Speaker(**response_data)


class AsyncSessionsMixin:
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
        response_data = await self._get(
            f"events/{event_identifier}/sessions/{session_id}"
        )
        return Session(**response_data)


class AsyncTracksMixin:
    """Async methods for Tracks."""

    async def get_event_tracks(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> TrackList:
        """Retrieves paginated tracks for an event (Async)."""
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/tracks", params=params
        )
        return TrackList(**response_data)

    async def get_track(self, event_identifier: str, track_id: str) -> Track:
        """Fetches a single track (Async)."""
        response_data = await self._get(f"events/{event_identifier}/tracks/{track_id}")
        return Track(**response_data)


class AsyncMicrolocationsMixin:
    """Async methods for Microlocations."""

    async def get_event_microlocations(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> MicrolocationList:
        """Retrieves paginated microlocations for an event (Async)."""
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/microlocations", params=params
        )
        return MicrolocationList(**response_data)

    async def get_microlocation(
        self, event_identifier: str, microlocation_id: str
    ) -> Microlocation:
        """Fetches a single microlocation (Async)."""
        response_data = await self._get(
            f"events/{event_identifier}/microlocations/{microlocation_id}"
        )
        return Microlocation(**response_data)


class AsyncSponsorsMixin:
    """Async methods for Sponsors."""

    async def get_event_sponsors(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> SponsorList:
        """Retrieves paginated sponsors for an event (Async)."""
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/sponsors", params=params
        )
        return SponsorList(**response_data)

    async def get_sponsor(self, event_identifier: str, sponsor_id: str) -> Sponsor:
        """Fetches a single sponsor (Async)."""
        response_data = await self._get(
            f"events/{event_identifier}/sponsors/{sponsor_id}"
        )
        return Sponsor(**response_data)


class AsyncDiscountCodesMixin:
    """Async methods for Discount Codes."""

    async def get_event_discount_codes(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> DiscountCodeList:
        """Retrieves paginated discount codes for an event (Async)."""
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/discount-codes", params=params
        )
        return DiscountCodeList(**response_data)

    async def get_discount_code(
        self, event_identifier: str, code_id: str
    ) -> DiscountCode:
        """Fetches a single discount code (Async)."""
        response_data = await self._get(
            f"events/{event_identifier}/discount-codes/{code_id}"
        )
        return DiscountCode(**response_data)


class AsyncOrdersMixin:
    """Async methods for Orders."""

    async def get_event_orders(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> OrderList:
        """Retrieves paginated orders for an event (Async)."""
        params = {"page": page, "page_size": page_size}
        response_data = await self._get(
            f"events/{event_identifier}/orders", params=params
        )
        return OrderList(**response_data)

    async def get_order(self, event_identifier: str, order_identifier: str) -> Order:
        """Fetches a single order (Async)."""
        response_data = await self._get(
            f"events/{event_identifier}/orders/{order_identifier}"
        )
        return Order(**response_data)


class AsyncTaxMixin:
    """Async methods for Tax."""

    async def get_event_tax(self, event_identifier: str) -> Tax:
        """Retrieves the tax configuration for an event (Async)."""
        response_data = await self._get(f"events/{event_identifier}/tax")
        return Tax(**response_data)


class AsyncUsersMixin:
    """Async methods for Users."""

    async def get_users(self, page: int = 1, page_size: int = 25) -> UserList:
        """
        Fetch all users (Async). Requires Admin.

        Returns:
            UserList object.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response = await self._get("users", params=params)
        return UserList(**response)

    async def get_user(self, user_id: str) -> User:
        """
        Get details of a specific user (Async).

        Args:
            user_id: The ID of the user.

        Returns:
            User object.
        """
        response = await self._get(f"users/{user_id}")
        return User(**response["data"])

    async def update_user(self, user_id: str, payload: Dict[str, Any]) -> User:
        """
        Update an existing user (Async).

        Args:
            user_id: The ID of the user.
            payload: JSON patch payload.

        Returns:
            Updated User object.
        """
        app_json = {"data": {"type": "user", "id": str(user_id), "attributes": payload}}
        response = await self._patch(f"users/{user_id}", json=app_json)
        return User(**response["data"])


class AsyncRolesMixin:
    """Async methods for Roles."""

    async def get_event_roles(
        self, event_id: str, page: int = 1, page_size: int = 25
    ) -> RoleList:
        """Fetch roles for an event (Async)."""
        params = {"page[number]": page, "page[size]": page_size}
        response = await self._get(
            f"events/{event_id}/roles", params=params
        )
        return RoleList(**response)

    async def get_role(self, event_id: str, role_id: str) -> Role:
        """Get a single role (Async)."""
        response = await self._get(
            f"events/{event_id}/roles/{role_id}"
        )
        return Role(**response["data"])
