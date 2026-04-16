from ._transport import SyncTransportBase
from .models import Page, PageList
from .utils import parse_jsonapi_list, parse_jsonapi_resource


class PagesMixin(SyncTransportBase):
    """Mixin class for interacting with Page endpoints."""

    def get_pages(self, page: int = 1, page_size: int = 25) -> PageList:
        """Retrieve paginated pages."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("pages", params=params)
        return PageList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_page(self, page_id: str) -> Page:
        """Fetch a single page by ID."""
        response_data = self._get(f"pages/{page_id}")
        return Page(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )
