from ._transport import SyncTransportBase
from .models import Service, ServiceList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class ServicesMixin(SyncTransportBase):
    """Mixin class for interacting with Service endpoints."""

    def get_services(self, page: int = 1, page_size: int = 25) -> ServiceList:
        """Retrieve paginated services."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("services", params=params)
        return ServiceList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_service(self, service_id: str) -> Service:
        """Fetch a single service by ID."""
        response_data = self._get(f"services/{service_id}")
        return Service(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
