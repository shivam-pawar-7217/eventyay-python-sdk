from typing import Dict, Any, Optional, List
from .utils import parse_pagination_params

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

    def get_all_events(self) -> List[Dict[str, Any]]:
        """
        Fetch ALL events by automatically iterating through pages.
        WARNING: This can take a long time for large datasets.
        
        Returns:
            Complete list of all event dictionaries.
        """
        all_events = []
        page = 1
        while True:
            response = self.get_events(page=page, page_size=50)
            data = response.get('data', [])
            if not data:
                break
            
            all_events.extend(data)
            
            links = response.get('links', {})
            next_url = links.get('next')
            if not next_url:
                break
                
            params = parse_pagination_params(next_url)
            next_page = params.get('page') or params.get('page[number]')
            if next_page:
                page = int(next_page)
            else:
                page += 1
                
        return all_events

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
