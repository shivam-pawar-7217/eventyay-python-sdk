"""
Events Mixin — Event-related API operations.

Handles listing, detail fetching, creation, update, and deletion of events,
as well as accessing event sub-resources (attendees, sessions, speakers).
"""

from typing import List, Optional

from .models import AttendeeList, Event, EventList, SessionList, SpeakerList
from .utils import (
    build_jsonapi_payload,
    parse_jsonapi_list,
    parse_jsonapi_resource,
    parse_pagination_params,
)


class EventsMixin:
    """
    Mixin class providing methods for interacting with Event-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_events(self, page: int = 1, page_size: int = 10) -> EventList:
        """
        Retrieves a paginated list of events.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of events per page. Defaults to 10.

        Returns:
            EventList: A Pydantic model containing the list of events and pagination metadata.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("events/", params=params)
        parsed = parse_jsonapi_list(response_data)
        return EventList(**parsed)

    def get_all_events(self) -> List[Event]:
        """
        Fetches all events from the API by automatically iterating through all pages.

        .. warning::
           This method can be slow for large datasets. Use with caution.

        Returns:
            List[Event]: A flat list of all Event objects.
        """
        all_events = []
        page = 1
        while True:
            response = self.get_events(page=page, page_size=50)
            data = response.data
            if not data:
                break

            all_events.extend(data)

            links = response.links or {}
            next_url = links.get("next")
            if not next_url:
                break

            params = parse_pagination_params(next_url)
            next_page = params.get("page[number]") or params.get("page")
            if next_page:
                page = int(next_page)
            else:
                page += 1

        return all_events

    def get_event(self, event_id: int) -> Event:
        """
        Fetches details for a single specific event.

        Args:
            event_id (int): The unique identifier of the event.

        Returns:
            Event: The detailed Event object.

        Raises:
            EventyayNotFoundError: If no event is found with the given ID.
        """
        response_data = self._get(f"events/{event_id}")
        parsed = parse_jsonapi_resource(response_data)
        return Event(**parsed)

    def get_event_attendees(
        self, event_id: str, page: int = 1, page_size: int = 10
    ) -> AttendeeList:
        """
        Retrieves a paginated list of attendees for a specific event.

        Args:
            event_id (str): The unique identifier of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of attendees per page. Defaults to 10.

        Returns:
            AttendeeList: A Pydantic model containing the list of attendees.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_id}/attendees", params=params)
        parsed = parse_jsonapi_list(response_data)
        return AttendeeList(**parsed)

    def get_event_sessions(self, event_id: str, page: int = 1) -> SessionList:
        """
        Retrieves a paginated list of sessions for a specific event.

        Args:
            event_id (str): The unique identifier of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Returns:
            SessionList: A Pydantic model containing the list of sessions.
        """
        params = {"page[number]": page}
        response_data = self._get(f"events/{event_id}/sessions", params=params)
        parsed = parse_jsonapi_list(response_data)
        return SessionList(**parsed)

    def get_event_speakers(self, event_id: str, page: int = 1) -> SpeakerList:
        """
        Retrieves a paginated list of speakers for a specific event.

        Args:
            event_id (str): The unique identifier of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Returns:
            SpeakerList: A Pydantic model containing the list of speakers.
        """
        params = {"page[number]": page}
        response_data = self._get(f"events/{event_id}/speakers", params=params)
        parsed = parse_jsonapi_list(response_data)
        return SpeakerList(**parsed)

    def create_event(
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
        Creates a new event.

        Args:
            name (str): The name of the event.
            identifier (str): A unique slug or identifier for the event.
            starts_at (str): Start time in ISO 8601 format.
            ends_at (str): End time in ISO 8601 format.
            timezone (str): Timezone string (e.g., 'UTC', 'Asia/Kolkata').
            privacy (str, optional): Event privacy. Defaults to "public".
            location_name (str, optional): Name of the physical location.
            online (bool, optional): Whether the event is virtual. Defaults to False.

        Returns:
            Event: The newly created Event object.
        """
        attributes = {
            "name": name,
            "identifier": identifier,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "timezone": timezone,
            "privacy": privacy,
            "online": online,
        }
        if location_name:
            attributes["location_name"] = location_name

        payload = build_jsonapi_payload("event", attributes)
        response_data = self._post("events", json=payload)
        parsed = parse_jsonapi_resource(response_data)
        return Event(**parsed)

    def update_event(
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
        Updates an existing event.

        Args:
            event_id (int): The unique identifier of the event to update.
            name (str, optional): New name.
            starts_at (str, optional): New start time.
            ends_at (str, optional): New end time.
            timezone (str, optional): New timezone.
            privacy (str, optional): New privacy setting.
            location_name (str, optional): New location name.

        Returns:
            Event: The updated Event object.
        """
        attributes = {}
        if name:
            attributes["name"] = name
        if starts_at:
            attributes["starts_at"] = starts_at
        if ends_at:
            attributes["ends_at"] = ends_at
        if timezone:
            attributes["timezone"] = timezone
        if privacy:
            attributes["privacy"] = privacy
        if location_name:
            attributes["location_name"] = location_name

        if not attributes:
            return self.get_event(event_id)

        payload = build_jsonapi_payload("event", attributes, resource_id=str(event_id))
        response_data = self._patch(f"events/{event_id}", json=payload)
        parsed = parse_jsonapi_resource(response_data)
        return Event(**parsed)

    def delete_event(self, event_id: int) -> bool:
        """
        Permanently deletes an event.

        Args:
            event_id (int): The unique identifier of the event to delete.

        Returns:
            bool: True if deletion was successful.
        """
        self._delete(f"events/{event_id}")
        return True
