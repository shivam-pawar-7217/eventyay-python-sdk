from typing import Dict, Any, Optional

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

    def get_organizer(self, organizer_id: int) -> Dict[str, Any]:
        """
        Get a single organizer by ID.
        
        Args:
            organizer_id: The ID of the organizer to retrieve
            
        Returns:
            Dictionary containing organizer details
        """
        return self._get(f'organizers/{organizer_id}')
