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
