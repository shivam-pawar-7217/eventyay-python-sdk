import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from eventyay import AsyncEventyayClient
from eventyay.models import Setting, SettingList

class TestAsyncSettings(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncEventyayClient(api_key="test_api_key")
        self.client._session = AsyncMock()

    @patch("eventyay.async_client.AsyncEventyayClient._request")
    async def test_get_settings(self, mock_request):
        mock_request.return_value = {
            "data": [
                {
                    "id": 1,
                    "app_environment": "production",
                    "app_name": "Eventyay",
                    "frontend_url": "https://eventyay.com"
                }
            ],
            "links": {"next": None},
            "meta": {"count": 1}
        }

        settings_list = await self.client.get_settings(page=1, page_size=10)
        
        mock_request.assert_awaited_once_with(
            "GET",
            "settings",
            params={"page[number]": 1, "page[size]": 10}
        )
        self.assertIsInstance(settings_list, SettingList)
        self.assertEqual(len(settings_list.data), 1)
        self.assertIsInstance(settings_list.data[0], Setting)
        self.assertEqual(settings_list.data[0].id, 1)
        self.assertEqual(settings_list.data[0].app_name, "Eventyay")

    @patch("eventyay.async_client.AsyncEventyayClient._request")
    async def test_get_setting(self, mock_request):
        mock_request.return_value = {
            "data": {
                "id": 1,
                "app_environment": "development",
                "app_name": "Dev Eventyay",
                "frontend_url": "https://dev.eventyay.com"
            }
        }

        setting = await self.client.get_setting("1")
        
        mock_request.assert_awaited_once_with(
            "GET",
            "settings/1",
            params={}
        )
        self.assertIsInstance(setting, Setting)
        self.assertEqual(setting.id, 1)
        self.assertEqual(setting.app_name, "Dev Eventyay")

if __name__ == '__main__':
    unittest.main()
