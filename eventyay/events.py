from typing import Dict, Any, Optional, List
from .utils import parse_pagination_params
from .models import Event, EventList, AttendeeList, SpeakerList, SessionList

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
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = self._get('events/', params=params)
        return EventList(**response_data)

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
        Fetches details for a single specific event.
        
        Args:
            event_id (int): The unique identifier of the event.
            
        Returns:
            Event: The detailed Event object.
            
        Raises:
            EventyayNotFoundError: If no event is found with the given ID.
        """
        response_data = self._get(f'events/{event_id}')
        return Event(**response_data)

    def get_event_attendees(self, event_id: str, page: int = 1, page_size: int = 10) -> AttendeeList:
        """
        Retrieves a paginated list of attendees for a specific event.

        Args:
            event_id (str): The unique identifier of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of attendees per page. Defaults to 10.

        Returns:
            AttendeeList: A Pydantic model containing the list of attendees.
        """
        params = {'page': page, 'page_size': page_size}
        response_data = self._get(f"events/{event_id}/attendees", params=params)
        return AttendeeList(**response_data)

    def get_event_sessions(self, event_id: str, page: int = 1) -> SessionList:
        """
        Retrieves a paginated list of sessions for a specific event.

        Args:
            event_id (str): The unique identifier of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Returns:
            SessionList: A Pydantic model containing the list of sessions.
        """
        params = {'page': page}
        response_data = self._get(f"events/{event_id}/sessions", params=params)
        return SessionList(**response_data)

    def get_event_speakers(self, event_id: str, page: int = 1) -> SpeakerList:
        """
        Retrieves a paginated list of speakers for a specific event.

        Args:
            event_id (str): The unique identifier of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Returns:
            SpeakerList: A Pydantic model containing the list of speakers.
        """
        params = {'page': page}
        response_data = self._get(f"events/{event_id}/speakers", params=params)
        return SpeakerList(**response_data)

    def create_event(self, name: str, identifier: str, starts_at: str, ends_at: str,
                    timezone: str, privacy: str = "public", location_name: Optional[str] = None,
                    online: bool = False) -> Event:
        """
        Creates a new event.
        
        Args:
            name (str): The name of the event.
            identifier (str): A unique slug or identifier for the event.
            starts_at (str): Start time in ISO 8601 format.
            ends_at (str): End time in ISO 8601 format.
            timezone (str): Timezone string (e.g., 'UTC', 'Asia/Kolkata').
            privacy (str, optional): Event privacy setting ('public' or 'private'). Defaults to "public".
            location_name (str, optional): Name of the physical location.
            online (bool, optional): Whether the event is virtual. Defaults to False.
            
        Returns:
            Event: The newly created Event object.
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
        Permanently deletes an event.
        
        Args:
            event_id (int): The unique identifier of the event to delete.
            
        Returns:
            bool: True if deletion was successful.
        """
        self._delete(f'events/{event_id}')
        return True
