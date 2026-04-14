from .models import Ticket, TicketList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class TicketsMixin:
    """
    Mixin class providing methods for interacting with Ticket-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_tickets(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> TicketList:
        """
        Retrieves a paginated list of tickets for a specific event.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of tickets per page. Defaults to 10.

        Returns:
            TicketList: A Pydantic model containing the list of tickets and pagination metadata.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_identifier}/tickets", params=params)
        return TicketList(**parse_jsonapi_list(response_data))

    def get_ticket(self, event_identifier: str, ticket_id: str) -> Ticket:
        """
        Fetches details for a single specific ticket.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            ticket_id (str): The unique identifier of the ticket.

        Returns:
            Ticket: The detailed Ticket object.

        Raises:
            EventyayNotFoundError: If no ticket is found with the given ID.
        """
        response_data = self._get(f"events/{event_identifier}/tickets/{ticket_id}")
        return Ticket(**parse_jsonapi_resource(response_data))
