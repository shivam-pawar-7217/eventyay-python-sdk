from typing import Optional
from .models import Session

class SessionsMixin:
    """
    Mixin class providing methods for interacting with standalone Session endpoints.
    
    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_session(self, event_identifier: str, session_id: str) -> Session:
        """
        Fetches details for a single specific session.
        
        Args:
            event_identifier (str): The unique identifier or slug of the event.
            session_id (str): The unique identifier of the session.
            
        Returns:
            Session: The detailed Session object.
        """
        response_data = self._get(f'events/{event_identifier}/sessions/{session_id}')
        return Session(**response_data)
