from typing import Dict, Any, Optional, List
from .utils import parse_pagination_params

class OrganizersMixin:
    """Mixin for Organizer-related API methods."""

    def get_organizers(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a list of organizers.
        
        Args:
            page: Page number (default: 1)
            page_size: Number of results per page (default: 10)
            
        Returns:
            Dictionary containing organizers data and pagination info
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        return self._get('organizers/', params=params)

    def get_all_organizers(self) -> List[Dict[str, Any]]:
        """
        Fetch ALL organizers by automatically iterating through pages.
        WARNING: This can take a long time for large datasets.
        
        Returns:
            Complete list of all organizer dictionaries.
        """
        all_organizers = []
        page = 1
        while True:
            response = self.get_organizers(page=page, page_size=50) # Maximize page size
            data = response.get('data', [])
            if not data:
                break
            
            all_organizers.extend(data)
            
            # Check for next page
            links = response.get('links', {})
            next_url = links.get('next')
            if not next_url:
                break
                
            # Parse next page number
            params = parse_pagination_params(next_url)
            # The key might be 'page' or 'page[number]'
            next_page = params.get('page') or params.get('page[number]')
            if next_page:
                page = int(next_page)
            else:
                # Fallback: just increment if no next link parsing but data exists?
                # Actually if next_url exists but parsing fails, we might be stuck.
                # Safe fallback: increment page
                page += 1
                
        return all_organizers

    def get_organizer(self, organizer_id: str) -> Dict[str, Any]:
        """
        Get details of a specific organizer.

        Args:
            organizer_id: The ID of the organizer.

        Returns:
            Dict containing organizer details.
        """
        return self._get(f"organizers/{organizer_id}")

    def get_organizer_events(self, organizer_id: str) -> list[Dict[str, Any]]:
        """
        Get all events for a specific organizer.

        Args:
            organizer_id: The ID of the organizer.

        Returns:
            List of events.
        """
        return self._get(f"organizers/{organizer_id}/events")

