from typing import Optional, Dict, Any
from .models import User, UserList


class UsersMixin:
    """
    Mixin for User-related API endpoints.
    Requires self._get() and self._patch() to be provided by the central client.
    """

    def get_users(self, page: int = 1, page_size: int = 25) -> UserList:
        """
        Retrieves a paginated list of users.
        NOTE: Requires administrative privileges.

        Args:
            page (int): The page number to fetch.
            page_size (int): Number of results per page.

        Returns:
            UserList: A paginated object containing a list of `User` objects.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response = self._get("users", params=params)
        return UserList(**response)

    def get_all_users(self) -> list[User]:
        """
        Helper method to exhaustively fetch all users across all pages.
        NOTE: Can be slow for instances with thousands of users.

        Returns:
            list[User]: A complete list of all users.
        """
        all_users = []
        page = 1
        while True:
            response = self.get_users(page=page, page_size=100)
            all_users.extend(response.data)

            if not response.links or not response.links.get("next"):
                break
            page += 1

        return all_users

    def get_user(self, user_id: str) -> User:
        """
        Retrieves details for a specific user.

        Args:
            user_id (str): The ID of the user (e.g., '1' or 'me').

        Returns:
            User: A parsed Pydantic `User` object.
        """
        response = self._get(f"users/{user_id}")
        return User(**response["data"])

    def update_user(self, user_id: str, payload: Dict[str, Any]) -> User:
        """
        Updates a specific user's details.

        Args:
            user_id (str): The ID of the user.
            payload (Dict[str, Any]): The JSON payload containing fields to update.

        Returns:
            User: The updated `User` object.
        """
        app_json = {"data": {"type": "user", "id": str(user_id), "attributes": payload}}
        response = self._patch(f"users/{user_id}", json=app_json)
        return User(**response["data"])
