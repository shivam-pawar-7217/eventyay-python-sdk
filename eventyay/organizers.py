from typing import Dict, Any, Optional, List
from .utils import parse_pagination_params
from .models import Organizer, OrganizerList, EventList, Event


class OrganizersMixin:
    """
    Mixin class providing methods for interacting with Organizer-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_organizers(self, page: int = 1, page_size: int = 10) -> OrganizerList:
        """
        Retrieves a paginated list of organizers.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of organizers per page. Defaults to 10.

        Returns:
            OrganizerList: A Pydantic model containing the list of organizers and pagination metadata.
        """
        params = {"page": page, "page_size": page_size}
        response_data = self._get("organizers/", params=params)
        return OrganizerList(**response_data)

    def get_all_organizers(self) -> List[Organizer]:
        """
        Fetches all organizers from the API by automatically iterating through all pages.

        .. warning::
           This method can be slow and may consume significant bandwidth/API quota
           if there are a large number of organizers.

        Returns:
            List[Organizer]: A complete flat list of all Organizer objects.
        """
        all_organizers = []
        page = 1
        while True:
            response = self.get_organizers(page=page, page_size=50)
            data = response.data
            if not data:
                break

            all_organizers.extend(data)

            links = response.links or {}
            next_url = links.get("next")
            if not next_url:
                break

            params = parse_pagination_params(next_url)
            next_page = params.get("page") or params.get("page[number]")
            if next_page:
                page = int(next_page)
            else:
                page += 1

        return all_organizers

    def get_organizer(self, organizer_id: str) -> Organizer:
        """
        Fetches details for a single specific organizer.

        Args:
            organizer_id (str): The unique identifier of the organizer.

        Returns:
            Organizer: The detailed Organizer object.

        Raises:
            EventyayNotFoundError: If no organizer is found with the given ID.
        """
        response_data = self._get(f"organizers/{organizer_id}")
        return Organizer(**response_data)

    def get_organizer_events(self, organizer_id: str, page: int = 1) -> EventList:
        """
        Retrieves a paginated list of events belonging to a specific organizer.

        Args:
            organizer_id (str): The unique identifier of the organizer.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Returns:
            EventList: A Pydantic model containing the list of events and pagination metadata.
        """
        params = {"page": page}
        response_data = self._get(f"organizers/{organizer_id}/events", params=params)
        return EventList(**response_data)

    def create_organizer(
        self,
        name: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        logo_url: Optional[str] = None,
    ) -> Organizer:
        """
        Creates a new organizer.

        Args:
            name (str): The name of the organizer.
            description (str, optional): A brief description of the organizer.
            url (str, optional): The official website URL of the organizer.
            logo_url (str, optional): A URL pointing to the organizer's logo image.

        Returns:
            Organizer: The newly created Organizer object as returned by the API.
        """
        data = {"name": name}
        if description:
            data["description"] = description
        if url:
            data["url"] = url
        if logo_url:
            data["logo_url"] = logo_url

        response_data = self._post("organizers", json=data)
        return Organizer(**response_data)

    def update_organizer(
        self,
        organizer_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        logo_url: Optional[str] = None,
    ) -> Organizer:
        """
        Updates an existing organizer's information (Partial updates supported).

        Args:
            organizer_id (str): The unique identifier of the organizer to update.
            name (str, optional): The new name for the organizer.
            description (str, optional): The new description.
            url (str, optional): The new website URL.
            logo_url (str, optional): The new logo URL.

        Returns:
            Organizer: The updated Organizer object.
        """
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if url:
            data["url"] = url
        if logo_url:
            data["logo_url"] = logo_url

        if not data:
            # No updates provided, return current state
            return self.get_organizer(organizer_id)

        response_data = self._patch(f"organizers/{organizer_id}", json=data)
        return Organizer(**response_data)

    def delete_organizer(self, organizer_id: str) -> bool:
        """
        Permanently deletes an organizer from the system.

        Args:
            organizer_id (str): The unique identifier of the organizer to delete.

        Returns:
            bool: Always True if the request was successful (204 No Content).

        Raises:
            EventyayAPIError: If the deletion fails.
        """
        self._delete(f"organizers/{organizer_id}")
        return True
