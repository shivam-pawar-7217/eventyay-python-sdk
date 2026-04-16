from ._transport import SyncTransportBase
from .models import AccessCode, AccessCodeList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class AccessCodesMixin(SyncTransportBase):
    """Mixin class for interacting with Access Code endpoints."""

    def get_event_access_codes(
        self, event_identifier: str, page: int = 1, page_size: int = 10
    ) -> AccessCodeList:
        """Retrieve access codes for an event."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_identifier}/access-codes", params=params)
        return AccessCodeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_ticket_access_codes(
        self, ticket_id: str, page: int = 1, page_size: int = 10
    ) -> AccessCodeList:
        """Retrieve access codes associated with a ticket."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"tickets/{ticket_id}/access-codes", params=params)
        return AccessCodeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_user_access_codes(self, user_id: str, page: int = 1, page_size: int = 10) -> AccessCodeList:
        """Retrieve access codes for a specific user."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"users/{user_id}/access-codes", params=params)
        return AccessCodeList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_access_code(self, access_code_id: str) -> AccessCode:
        """Fetch a single access code by ID."""
        response_data = self._get(f"access-codes/{access_code_id}")
        return AccessCode(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_access_code_by_code(self, code: str) -> AccessCode:
        """Fetch access code details by code value."""
        response_data = self._get(f"access-codes/{code}")
        return AccessCode(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
