"""Tests for Settings-related operations."""

from eventyay.models import Setting, SettingList


class TestGetSettings:
    def test_returns_setting_list(self, mock_client, mock_response, sample_setting):
        mock_client.session.get.return_value = mock_response({"data": [sample_setting]})

        result = mock_client.get_settings()

        assert isinstance(result, SettingList)
        assert len(result.data) == 1
        assert result.data[0].app_name == "Eventyay"


class TestGetSetting:
    def test_returns_setting(self, mock_client, mock_response, sample_setting):
        mock_client.session.get.return_value = mock_response({"data": sample_setting})

        result = mock_client.get_setting("1401")

        assert isinstance(result, Setting)
        assert result.app_environment == "production"
        assert result.frontend_url == "https://eventyay.com"
