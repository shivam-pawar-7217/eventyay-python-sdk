from .models import Tax


class TaxMixin:
    """
    Mixin class for interacting with Tax-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_tax(self, event_identifier: str) -> Tax:
        """
        Retrieves the tax configuration for a specific event.

        Args:
            event_identifier: The unique identifier or slug of the event.

        Returns:
            Tax: The tax configuration object.
        """
        response_data = self._get(f"events/{event_identifier}/tax")
        return Tax(**response_data)
