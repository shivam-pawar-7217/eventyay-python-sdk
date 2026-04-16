from ._transport import SyncTransportBase
from .models import Role, RoleList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class RolesMixin(SyncTransportBase):
    """
    Mixin for Role-related API endpoints.
    Requires self._get() to be provided by the central client.
    """

    def get_event_roles(self, event_id: str, page: int = 1, page_size: int = 25) -> RoleList:
        """
        Retrieves a paginated list of roles for an event.

        Args:
            event_id (str): The event identifier.
            page (int): The page number to fetch.
            page_size (int): Number of results per page.

        Returns:
            RoleList: A paginated object containing `Role` objects.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get(f"events/{event_id}/roles", params=params)
        return RoleList(**parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False)))

    def get_role(self, event_id: str, role_id: str) -> Role:
        """
        Retrieves details of a single role.

        Args:
            event_id (str): The event identifier.
            role_id (str): The ID of the role.

        Returns:
            Role: A parsed Pydantic `Role` object.
        """
        response_data = self._get(f"events/{event_id}/roles/{role_id}")
        return Role(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))
