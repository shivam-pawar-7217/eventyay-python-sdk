from typing import List, Dict, Any, Optional

class AsyncOrganizersMixin:
    """Async methods for Organizers."""
    
    async def get_organizers(self) -> List[Dict[str, Any]]:
        """
        Fetch all organizers (Async).
        
        Returns:
            List of organizer dictionaries.
        """
        return await self._get("organizers")

    async def get_organizer(self, organizer_id: str) -> Dict[str, Any]:
        """
        Get details of a specific organizer (Async).

        Args:
            organizer_id: The ID of the organizer.

        Returns:
            Dict containing organizer details.
        """
        return await self._get(f"organizers/{organizer_id}")

class AsyncEventsMixin:
    """Async methods for Events."""
    
    async def get_events(self) -> List[Dict[str, Any]]:
        """
        Fetch all public events (Async).
        
        Returns:
            List of event dictionaries.
        """
        return await self._get("events")

    async def get_event(self, event_id: int) -> Dict[str, Any]:
        """
        Get a single event by ID (Async).

        Args:
            event_id: The ID of the event to retrieve.

        Returns:
            Dictionary containing event details.
        """
        return await self._get(f"events/{event_id}")

    async def get_event_attendees(self, event_id: str) -> List[Dict[str, Any]]:
        """
        Get all attendees for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            List of attendee dictionaries.
        """
        return await self._get(f"events/{event_id}/attendees")

    async def get_event_speakers(self, event_id: str) -> List[Dict[str, Any]]:
        """
        Get all speakers for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            List of speaker dictionaries.
        """
        return await self._get(f"events/{event_id}/speakers")

    async def get_event_sessions(self, event_id: str) -> List[Dict[str, Any]]:
        """
        Get all sessions (talks) for a specific event (Async).

        Args:
            event_id: The ID of the event.

        Returns:
            List of session dictionaries.
        """
        return await self._get(f"events/{event_id}/sessions")
