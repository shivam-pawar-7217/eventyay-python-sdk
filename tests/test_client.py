"""Tests for the synchronous EventyayClient."""

import pytest

from eventyay.access_codes import AccessCodesMixin
from eventyay.attendees import AttendeesMixin
from eventyay.auth import AuthMixin
from eventyay.client import EventyayClient
from eventyay.event_sub_topics import EventSubTopicsMixin
from eventyay.event_topics import EventTopicsMixin
from eventyay.event_types import EventTypesMixin
from eventyay.exceptions import EventyayValidationError
from eventyay.misc_resources import MiscResourcesMixin
from eventyay.notifications import NotificationsMixin
from eventyay.pages import PagesMixin
from eventyay.role_invites import RoleInvitesMixin
from eventyay.services import ServicesMixin
from eventyay.ticket_tags import TicketTagsMixin


class TestClientInit:
    def test_default_init(self):
        client = EventyayClient()
        assert "api.eventyay.com" in client.base_url
        assert client.api_key is None
        assert client.timeout == 30

    def test_with_api_key(self):
        client = EventyayClient(api_key="test-key-1234")
        assert client.session.headers["Authorization"] == "Token test-key-1234"

    def test_custom_timeout(self):
        client = EventyayClient(timeout=60)
        assert client.timeout == 60

    def test_repr_masks_key(self):
        client = EventyayClient(api_key="secret_key_12345")
        assert "secr..." in repr(client)
        assert "secret_key_12345" not in repr(client)

    def test_repr_no_key(self):
        client = EventyayClient()
        assert "None" in repr(client)


class TestClientContextManager:
    def test_context_manager(self):
        with EventyayClient(api_key="test") as client:
            assert client.session is not None


class TestClientHeaders:
    def test_default_headers(self):
        client = EventyayClient()
        assert client.session.headers["Content-Type"] == "application/vnd.api+json"
        assert client.session.headers["Accept"] == "application/vnd.api+json"

    def test_no_auth_header_without_key(self):
        client = EventyayClient()
        assert "Authorization" not in client.session.headers


class TestClientBaseUrl:
    def test_strips_trailing_slash(self):
        client = EventyayClient(base_url="https://api.example.com/v1/")
        assert client.base_url == "https://api.example.com/v1"


class TestClientMethodResolution:
    def test_get_event_attendees_resolves_to_attendees_mixin(self):
        assert EventyayClient.get_event_attendees is AttendeesMixin.get_event_attendees

    def test_get_event_access_codes_resolves_to_access_codes_mixin(self):
        assert EventyayClient.get_event_access_codes is AccessCodesMixin.get_event_access_codes

    def test_get_role_invites_resolves_to_role_invites_mixin(self):
        assert EventyayClient.get_role_invites is RoleInvitesMixin.get_role_invites

    def test_get_event_ticket_tags_resolves_to_ticket_tags_mixin(self):
        assert EventyayClient.get_event_ticket_tags is TicketTagsMixin.get_event_ticket_tags

    def test_get_event_types_resolves_to_event_types_mixin(self):
        assert EventyayClient.get_event_types is EventTypesMixin.get_event_types

    def test_get_event_topics_resolves_to_event_topics_mixin(self):
        assert EventyayClient.get_event_topics is EventTopicsMixin.get_event_topics

    def test_get_event_sub_topics_resolves_to_event_sub_topics_mixin(self):
        assert EventyayClient.get_event_sub_topics is EventSubTopicsMixin.get_event_sub_topics

    def test_get_notifications_resolves_to_notifications_mixin(self):
        assert EventyayClient.get_notifications is NotificationsMixin.get_notifications

    def test_get_pages_resolves_to_pages_mixin(self):
        assert EventyayClient.get_pages is PagesMixin.get_pages

    def test_get_services_resolves_to_services_mixin(self):
        assert EventyayClient.get_services is ServicesMixin.get_services

    def test_get_activities_resolves_to_misc_resources_mixin(self):
        assert EventyayClient.get_activities is MiscResourcesMixin.get_activities

    def test_login_resolves_to_auth_mixin(self):
        assert EventyayClient.login is AuthMixin.login


class TestClientEndpointValidation:
    def test_rejects_absolute_url_endpoints(self, mock_client):
        with pytest.raises(EventyayValidationError):
            mock_client._get("https://evil.example/path")

        mock_client.session.get.assert_not_called()

    def test_rejects_bidi_control_chars(self, mock_client):
        with pytest.raises(EventyayValidationError):
            mock_client._get("events/\u202Eabc")

        mock_client.session.get.assert_not_called()
