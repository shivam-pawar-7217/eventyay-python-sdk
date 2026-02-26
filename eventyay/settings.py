from typing import Optional, Any
from .models import Setting, SettingList

class SettingsMixin:
    """
    Mixin for Eventyay settings operations.
    Should be inherited by the main EventyayClient.
    """

    def get_settings(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs: Any,
    ) -> SettingList:
        """
        Get a paginated list of global settings.

        Args:
            page (Optional[int]): The page number to retrieve. Defaults to None.
            page_size (Optional[int]): The number of items per page. Defaults to None.
            **kwargs: Additional query parameters (e.g., filter, sort).

        Returns:
            SettingList: A paginated list of settings.
        """
        params = kwargs.copy()
        if page is not None:
            params["page[number]"] = page
        if page_size is not None:
            params["page[size]"] = page_size

        response_data = self._get("settings", params=params)
        return SettingList(**response_data)

    def get_setting(self, setting_id: str, **kwargs: Any) -> Setting:
        """
        Get a specific setting by ID.

        Args:
            setting_id (str): The ID of the setting.
            **kwargs: Additional query parameters.

        Returns:
            Setting: The setting details.
        """
        response_data = self._get(f"settings/{setting_id}", params=kwargs)
        return Setting(**response_data["data"])
