"""Tests for Notification related operations."""

from eventyay.models import Notification, NotificationList


class TestGetNotifications:
    def test_returns_notification_list(self, mock_client, mock_response, sample_notification):
        mock_client.session.get.return_value = mock_response({"data": [sample_notification]})

        result = mock_client.get_notifications()

        assert isinstance(result, NotificationList)
        assert len(result.data) == 1
        assert result.data[0].title == "Welcome"


class TestGetNotification:
    def test_returns_notification(self, mock_client, mock_response, sample_notification):
        mock_client.session.get.return_value = mock_response(sample_notification)

        result = mock_client.get_notification("1701")

        assert isinstance(result, Notification)
        assert result.id == 1701
