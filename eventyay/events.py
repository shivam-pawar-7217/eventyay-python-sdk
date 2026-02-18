from typing import Dict, Any, Optional, List
from .utils import parse_pagination_params
from .models import Event, EventList, AttendeeList, SpeakerList, SessionList

class EventsMixin:
    """Mixin for Event-related API methods."""

    def get_events(self, page: int = 1, page_size: int = 10) -> EventList:
        """
        Get a list of events.
        
        Args:
            page: Page number (default: 1)
            page_size: Number of results per page (default: 10)
            
        Returns:
            EventList object containing data (list of Events) and pagination info.
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = self._get('events/', params=params)
        return EventList(**response_data)

    def get_all_events(self) -> List[Event]:
        """
        Fetch ALL events by automatically iterating through pages.
        WARNING: This can take a long time for large datasets.
        
        Returns:
            Complete list of all Event objects.
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

    def get_event(self, event_id: int) -> Event:
        """
        Get a single event by ID.
        
        Args:
            event_id: The ID of the event to retrieve
            
        Returns:
            Event object.
        """
        response_data = self._get(f'events/{event_id}')
        return Event(**response_data)

    def get_event_attendees(self, event_id: str, page: int = 1) -> AttendeeList:
        """
        Get all attendees for a specific event.

        Args:
            event_id: The ID of the event.
            page: Page number (default: 1).

        Returns:
            AttendeeList object.
        """
        params = {'page': page}
        response_data = self._get(f"events/{event_id}/attendees", params=params)
        return AttendeeList(**response_data)

    def get_event_sessions(self, event_id: str, page: int = 1) -> SessionList:
        """
        Get all sessions (talks) for a specific event.

        Args:
            event_id: The ID of the event.
            page: Page number (default: 1).

        Returns:
            SessionList object.
        """
        params = {'page': page}
        response_data = self._get(f"events/{event_id}/sessions", params=params)
        return SessionList(**response_data)

    def get_event_speakers(self, event_id: str, page: int = 1) -> SpeakerList:
        """
        Get all speakers for a specific event.

        Args:
            event_id: The ID of the event.
            page: Page number (default: 1).

        Returns:
            SpeakerList object.
        """
        params = {'page': page}
        response_data = self._get(f"events/{event_id}/speakers", params=params)
        return SpeakerList(**response_data)
