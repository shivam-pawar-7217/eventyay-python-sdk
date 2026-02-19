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

    def create_organizer(self, name: str, description: Optional[str] = None, 
                        url: Optional[str] = None, logo_url: Optional[str] = None) -> Organizer:
        """
        Create a new organizer.
        
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
        
        response_data = self._post('organizers', json=data)
        return Organizer(**response_data)

    def update_organizer(self, organizer_id: str, name: Optional[str] = None, 
                        description: Optional[str] = None, url: Optional[str] = None, 
                        logo_url: Optional[str] = None) -> Organizer:
        """
        Update an existing organizer.
        
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
            # No updates provided, return current state
            return self.get_organizer(organizer_id)
            
        response_data = self._patch(f'organizers/{organizer_id}', json=data)
        return Organizer(**response_data)

    def delete_organizer(self, organizer_id: str) -> bool:
        """
        Delete an organizer.
        
        Args:
            organizer_id: The ID of the organizer to delete.
            
        Returns:
            True if deletion was successful.
        """
        self._delete(f'organizers/{organizer_id}')
        return True
