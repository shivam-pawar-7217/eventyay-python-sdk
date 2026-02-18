from typing import Dict, Any, Optional, List
from .utils import parse_pagination_params
from .models import Organizer, OrganizerList, EventList, Event

class OrganizersMixin:
    """Mixin for Organizer-related API methods."""

    def get_organizers(self, page: int = 1, page_size: int = 10) -> OrganizerList:
        """
        Get a list of organizers.
        
        Args:
            page: Page number (default: 1)
            page_size: Number of results per page (default: 10)
            
        Returns:
            OrganizerList object containing data (list of Organizers) and pagination info.
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = self._get('organizers/', params=params)
        return OrganizerList(**response_data)

    def get_all_organizers(self) -> List[Organizer]:
        """
        Fetch ALL organizers by automatically iterating through pages.
        WARNING: This can take a long time for large datasets.
        
        Returns:
            Complete list of all Organizer objects.
        """
        all_organizers = []
        page = 1
        while True:
            response = self.get_organizers(page=page, page_size=50) 
            data = response.data
            if not data:
                break
            
            all_organizers.extend(data)
            
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
                
        return all_organizers

    def get_organizer(self, organizer_id: str) -> Organizer:
        """
        Get details of a specific organizer.
        
        Args:
            organizer_id: The ID of the organizer.
            
        Returns:
            Organizer object.
        """
        response_data = self._get(f'organizers/{organizer_id}')
        return Organizer(**response_data)

    def get_organizer_events(self, organizer_id: str, page: int = 1) -> EventList:
        """
        Get all events for a specific organizer.

        Args:
            organizer_id: The ID of the organizer.
            page: Page number (default: 1).

        Returns:
            EventList object containing events and pagination info.
        """
        params = {'page': page}
        response_data = self._get(f"organizers/{organizer_id}/events", params=params)
        return EventList(**response_data)
