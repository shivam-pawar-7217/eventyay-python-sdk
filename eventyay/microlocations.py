from .models import Microlocation, MicrolocationList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class MicrolocationsMixin:
    """
    Mixin class for interacting with Microlocation-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_microlocations(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> MicrolocationList:
        """
        Retrieves a paginated list of microlocations for a specific event.

        Args:
            event_identifier: The unique identifier or slug of the event.
            page: The page number to retrieve. Defaults to 1.
            page_size: Number of items per page. Defaults to 10.

        Returns:
            MicrolocationList: Paginated list of microlocations.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_identifier}/microlocations", params=params)
        return MicrolocationList(**parse_jsonapi_list(response_data))

    def get_microlocation(self, event_identifier: str, microlocation_id: str) -> Microlocation:
        """
        Fetches details for a single specific microlocation.

        Args:
            event_identifier: The unique identifier or slug of the event.
            microlocation_id: The unique identifier of the microlocation.

        Returns:
            Microlocation: The detailed Microlocation object.
        """
        response_data = self._get(f"events/{event_identifier}/microlocations/{microlocation_id}")
        return Microlocation(**parse_jsonapi_resource(response_data))
