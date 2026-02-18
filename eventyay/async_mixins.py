from typing import List, Dict, Any, Optional
from .models import (
    Organizer, OrganizerList,
    Event, EventList, AttendeeList, SpeakerList, SessionList
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

