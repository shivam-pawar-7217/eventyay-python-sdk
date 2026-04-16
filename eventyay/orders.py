from ._transport import SyncTransportBase
from .models import Order, OrderList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class OrdersMixin(SyncTransportBase):
    """
    Mixin class for interacting with Order-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_orders(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> OrderList:
        """
        Retrieves a paginated list of orders for a specific event.

        Args:
            event_identifier: The unique identifier or slug of the event.
            page: The page number to retrieve. Defaults to 1.
            page_size: Number of items per page. Defaults to 10.

        Returns:
            OrderList: Paginated list of orders.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_identifier}/orders", params=params)
        return OrderList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    def get_order(self, event_identifier: str, order_identifier: str) -> Order:
        """
        Fetches details for a single specific order.

        Args:
            event_identifier: The unique identifier or slug of the event.
            order_identifier: The unique identifier of the order.

        Returns:
            Order: The detailed Order object.
        """
        response_data = self._get(f"events/{event_identifier}/orders/{order_identifier}")
        return Order(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))
