from .models import Sponsor, SponsorList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class SponsorsMixin:
    """
    Mixin class for interacting with Sponsor-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_sponsors(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> SponsorList:
        """
        Retrieves a paginated list of sponsors for a specific event.

        Args:
            event_identifier: The unique identifier or slug of the event.
            page: The page number to retrieve. Defaults to 1.
            page_size: Number of items per page. Defaults to 10.

        Returns:
            SponsorList: Paginated list of sponsors.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_identifier}/sponsors", params=params)
        return SponsorList(**parse_jsonapi_list(response_data))

    def get_sponsor(self, event_identifier: str, sponsor_id: str) -> Sponsor:
        """
        Fetches details for a single specific sponsor.

        Args:
            event_identifier: The unique identifier or slug of the event.
            sponsor_id: The unique identifier of the sponsor.

        Returns:
            Sponsor: The detailed Sponsor object.
        """
        response_data = self._get(f"events/{event_identifier}/sponsors/{sponsor_id}")
        return Sponsor(**parse_jsonapi_resource(response_data))
