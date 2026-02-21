from typing import Optional
from .models import Attendee, AttendeeList

class AttendeesMixin:
    """
    Mixin class providing methods for interacting with Attendee-related endpoints.
    
    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_attendees(self, event_identifier: str, page: int = 1, page_size: int = 10) -> AttendeeList:
        """
        Retrieves a paginated list of attendees for a specific event.
        
        Args:
            event_identifier (str): The unique identifier or slug of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of attendees per page. Defaults to 10.
            
        Returns:
            AttendeeList: A Pydantic model containing the list of attendees and pagination metadata.
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = self._get(f'events/{event_identifier}/attendees', params=params)
        return AttendeeList(**response_data)

    def get_attendee(self, event_identifier: str, attendee_id: str) -> Attendee:
        """
        Fetches details for a single specific attendee.
        
        Args:
            event_identifier (str): The unique identifier or slug of the event.
            attendee_id (str): The unique identifier of the attendee.
            
        Returns:
            Attendee: The detailed Attendee object.
        """
        response_data = self._get(f'events/{event_identifier}/attendees/{attendee_id}')
        return Attendee(**response_data)
