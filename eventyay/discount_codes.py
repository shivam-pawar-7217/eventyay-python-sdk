from .models import DiscountCode, DiscountCodeList


class DiscountCodesMixin:
    """
    Mixin class for interacting with DiscountCode-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_discount_codes(
        self, event_identifier: str,
        page: int = 1, page_size: int = 10
    ) -> DiscountCodeList:
        """
        Retrieves discount codes available for a specific event.

        Args:
            event_identifier: The unique identifier or slug of the event.
            page: The page number to retrieve. Defaults to 1.
            page_size: Number of items per page. Defaults to 10.

        Returns:
            DiscountCodeList: Paginated list of discount codes.
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = self._get(
            f'events/{event_identifier}/discount-codes', params=params
        )
        return DiscountCodeList(**response_data)

    def get_discount_code(
        self, event_identifier: str, code_id: str
    ) -> DiscountCode:
        """
        Fetches details for a single discount code.

        Args:
            event_identifier: The unique identifier or slug of the event.
            code_id: The unique identifier of the discount code.

        Returns:
            DiscountCode: The detailed DiscountCode object.
        """
        response_data = self._get(
            f'events/{event_identifier}/discount-codes/{code_id}'
        )
        return DiscountCode(**response_data)
