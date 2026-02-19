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

    def create_event(self, name: str, identifier: str, starts_at: str, ends_at: str,
                    timezone: str, privacy: str = "public", location_name: Optional[str] = None,
                    online: bool = False) -> Event:
        """
        Create a new event.
        
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
        
        response_data = self._post('events', json=data)
        return Event(**response_data)

    def update_event(self, event_id: int, name: Optional[str] = None, 
                    starts_at: Optional[str] = None, ends_at: Optional[str] = None,
                    timezone: Optional[str] = None, privacy: Optional[str] = None,
                    location_name: Optional[str] = None) -> Event:
        """
        Update an existing event.
        
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
            return self.get_event(event_id)
            
        response_data = self._patch(f'events/{event_id}', json=data)
        return Event(**response_data)

    def delete_event(self, event_id: int) -> bool:
        """
        Delete an event.
        
        Args:
            event_id: The ID of the event.
            
        Returns:
            True if successful.
        """
        self._delete(f'events/{event_id}')
        return True
