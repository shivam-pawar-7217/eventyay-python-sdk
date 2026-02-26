import unittest
from unittest.mock import patch, MagicMock
from eventyay import EventyayClient
from eventyay.models import Setting, SettingList

class TestSettings(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_api_key")
        self.client.session = MagicMock()

    def test_get_settings(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
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
        self.client.session.get.return_value = mock_response

        settings_list = self.client.get_settings(page=1, page_size=10)
        
        self.client.session.get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/settings",
            params={"page[number]": 1, "page[size]": 10}
        )
        self.assertIsInstance(settings_list, SettingList)
        self.assertEqual(len(settings_list.data), 1)
        self.assertIsInstance(settings_list.data[0], Setting)
        self.assertEqual(settings_list.data[0].id, 1)
        self.assertEqual(settings_list.data[0].app_name, "Eventyay")

    def test_get_setting(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "app_environment": "development",
                "app_name": "Dev Eventyay",
                "frontend_url": "https://dev.eventyay.com"
            }
        }
        self.client.session.get.return_value = mock_response

        setting = self.client.get_setting("1")
        
        self.client.session.get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/settings/1",
            params={}
        )
        self.assertIsInstance(setting, Setting)
        self.assertEqual(setting.id, 1)
        self.assertEqual(setting.app_name, "Dev Eventyay")
        self.assertEqual(setting.app_environment, "development")

if __name__ == '__main__':
    unittest.main()
