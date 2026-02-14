from typing import List, Dict, Any, Optional

class AsyncOrganizersMixin:
    """Async methods for Organizers."""
    
    async def get_organizers(self) -> List[Dict[str, Any]]:
        """
        Fetch all organizers (Async).
        
        Returns:
            List of organizer dictionaries.
        """
        # We assume 'self' has a _get method or similar from the client
        # But wait, AsyncClient doesn't have _get yet?
        # AsyncClient uses direct aiohttp session calls in implementation.
        # We should probably add a helper _get method to AsyncClient or mixin.
        # For now, let's access self._session directly if we can, OR best practice:
        # Add `_get` to AsyncClient and use `await self._get(...)`.
        
        # Let's assume we will add `_get` to AsyncClient.
        return await self._get("organizers")

class AsyncEventsMixin:
    """Async methods for Events."""
    
    async def get_events(self) -> List[Dict[str, Any]]:
        """
        Fetch all public events (Async).
        
        Returns:
            List of event dictionaries.
        """
        return await self._get("events")
