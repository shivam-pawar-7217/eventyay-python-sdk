from typing import List, Dict, Any, Optional
from .models import (
    Organizer, OrganizerList,
    Event, EventList, AttendeeList, SpeakerList, SessionList,
    Ticket, TicketList
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
        params = {'page': page}
        response_data = await self._get(f"organizers/{organizer_id}/events", params=params)
        return EventList(**response_data)

    async def create_organizer(self, name: str, description: Optional[str] = None, 
                              url: Optional[str] = None, logo_url: Optional[str] = None) -> Organizer:
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
        data = {
            'name': name
        }
        if description: data['description'] = description
        if url: data['url'] = url
        if logo_url: data['logo_url'] = logo_url
        
        response_data = await self._post('organizers', json=data)
        return Organizer(**response_data)

    async def update_organizer(self, organizer_id: str, name: Optional[str] = None, 
                              description: Optional[str] = None, url: Optional[str] = None, 
                              logo_url: Optional[str] = None) -> Organizer:
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
        if name: data['name'] = name
        if description: data['description'] = description
        if url: data['url'] = url
        if logo_url: data['logo_url'] = logo_url
        
        if not data:
            return await self.get_organizer(organizer_id)
            
        response_data = await self._patch(f'organizers/{organizer_id}', json=data)
        return Organizer(**response_data)

    async def delete_organizer(self, organizer_id: str) -> bool:
        """
        Delete an organizer (Async).
        
        Args:
            organizer_id: The ID of the organizer to delete.
            
        Returns:
            True if deletion was successful.
        """
        await self._delete(f'organizers/{organizer_id}')
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

    async def create_event(self, name: str, identifier: str, starts_at: str, ends_at: str,
                          timezone: str, privacy: str = "public", location_name: Optional[str] = None,
                          online: bool = False) -> Event:
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
            'name': name,
            'identifier': identifier,
            'starts_at': starts_at,
            'ends_at': ends_at,
            'timezone': timezone,
            'privacy': privacy,
            'online': online
        }
        if location_name: data['location_name'] = location_name
        
        response_data = await self._post('events', json=data)
        return Event(**response_data)

    async def update_event(self, event_id: int, name: Optional[str] = None, 
                          starts_at: Optional[str] = None, ends_at: Optional[str] = None,
                          timezone: Optional[str] = None, privacy: Optional[str] = None,
                          location_name: Optional[str] = None) -> Event:
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
        if name: data['name'] = name
        if starts_at: data['starts_at'] = starts_at
        if ends_at: data['ends_at'] = ends_at
        if timezone: data['timezone'] = timezone
        if privacy: data['privacy'] = privacy
        if location_name: data['location_name'] = location_name
        
        if not data:
            return await self.get_event(event_id)
            
        response_data = await self._patch(f'events/{event_id}', json=data)
        return Event(**response_data)

    async def delete_event(self, event_id: int) -> bool:
        """
        Delete an event (Async).
        
        Args:
            event_id: The ID of the event.
            
        Returns:
            True if successful.
        """
        await self._delete(f'events/{event_id}')
        return True


class AsyncTicketsMixin:
    """Async methods for Tickets."""

    async def get_event_tickets(self, event_identifier: str, page: int = 1, page_size: int = 10) -> TicketList:
        """
        Retrieves a paginated list of tickets for a specific event (Async).
        
        Args:
            event_identifier (str): The unique identifier or slug of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of tickets per page. Defaults to 10.
            
        Returns:
            TicketList: A Pydantic model containing the list of tickets and pagination metadata.
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = await self._get(f'events/{event_identifier}/tickets', params=params)
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
        response_data = await self._get(f'events/{event_identifier}/tickets/{ticket_id}')
        return Ticket(**response_data)
