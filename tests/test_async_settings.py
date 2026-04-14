"""Tests for async settings operations."""

from unittest.mock import AsyncMock, patch

import pytest

from eventyay import AsyncEventyayClient
from eventyay.models import Setting, SettingList


class TestAsyncGetSettings:
    @pytest.mark.asyncio
    async def test_get_settings(self):
        client = AsyncEventyayClient(api_key="test_api_key")
        client._session = AsyncMock()

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "data": [
                    {
                        "id": 1,
                        "app_environment": "production",
                        "app_name": "Eventyay",
                        "frontend_url": "https://eventyay.com",
                    }
                ],
                "links": {"next": None},
                "meta": {"count": 1},
            }

            settings_list = await client.get_settings(page=1, page_size=10)

            assert isinstance(settings_list, SettingList)
            assert len(settings_list.data) == 1
            assert settings_list.data[0].app_name == "Eventyay"

    @pytest.mark.asyncio
    async def test_get_setting(self):
        client = AsyncEventyayClient(api_key="test_api_key")
        client._session = AsyncMock()

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "data": {
                    "id": 1,
                    "app_environment": "development",
                    "app_name": "Dev Eventyay",
                    "frontend_url": "https://dev.eventyay.com",
                }
            }

            setting = await client.get_setting("1")

            assert isinstance(setting, Setting)
            assert setting.app_name == "Dev Eventyay"
