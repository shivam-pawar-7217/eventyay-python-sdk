from typing import Dict, Any, Optional

class EventsMixin:
    """Mixin for Event-related API methods."""

    def get_events(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a list of events.
        
        Args:
            page: Page number (default: 1)
            page_size: Number of results per page (default: 10)
            
        Returns:
            Dictionary containing events data and pagination info
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        return self._get('events/', params=params)

    def get_event(self, event_id: int) -> Dict[str, Any]:
        """
        Get a single event by ID.
        
        Args:
            event_id: The ID of the event to retrieve
            
        Returns:
            Dictionary containing event details
        """
        return self._get(f'events/{event_id}')

    def get_event_attendees(self, event_id: str) -> list[Dict[str, Any]]:
        """
        Get all attendees for a specific event.

        Args:
            event_id: The ID of the event.

        Returns:
            List of attendees.
        """
        return self._get(f"events/{event_id}/attendees")

    def get_event_sessions(self, event_id: str) -> list[Dict[str, Any]]:
        """
        Get all sessions (talks) for a specific event.

        Args:
            event_id: The ID of the event.

        Returns:
            List of sessions.
        """
        return self._get(f"events/{event_id}/sessions")

    def get_event_speakers(self, event_id: str) -> list[Dict[str, Any]]:
        """
        Get all speakers for a specific event.

        Args:
            event_id: The ID of the event.

        Returns:
            List of speakers.
        """
        return self._get(f"events/{event_id}/speakers")
