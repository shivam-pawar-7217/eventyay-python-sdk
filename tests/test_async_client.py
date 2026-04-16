"""Tests for the AsyncEventyayClient."""

import asyncio
from unittest.mock import AsyncMock

import aiohttp
import pytest

from eventyay.async_client import AsyncEventyayClient
from eventyay.async_mixins import AsyncAccessCodesMixin
from eventyay.async_mixins import AsyncAttendeesMixin
from eventyay.async_mixins import AsyncAuthMixin
from eventyay.async_mixins import AsyncEventSubTopicsMixin
from eventyay.async_mixins import AsyncEventTopicsMixin
from eventyay.async_mixins import AsyncEventTypesMixin
from eventyay.async_mixins import AsyncMiscResourcesMixin
from eventyay.async_mixins import AsyncNotificationsMixin
from eventyay.async_mixins import AsyncPagesMixin
from eventyay.async_mixins import AsyncRoleInvitesMixin
from eventyay.async_mixins import AsyncServicesMixin
from eventyay.async_mixins import AsyncTicketTagsMixin
from eventyay.exceptions import EventyayConnectionError
from eventyay.exceptions import EventyayAPIError
from eventyay.exceptions import EventyayTimeoutError
from eventyay.exceptions import EventyayValidationError


class _FakeResponse:
    def __init__(self, status, json_data=None, text_data=""):
        self.status = status
        self._json_data = json_data if json_data is not None else {}
        self._text_data = text_data
        self.headers = {}

    async def json(self, *args, **kwargs):
        return self._json_data

    async def text(self):
        return self._text_data


class _FakeRequestContext:
    def __init__(self, response):
        self.response = response

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


class _FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0
        self.last_headers = None

    def request(self, method, url, params=None, json=None, headers=None):
        self.calls += 1
        self.last_headers = headers
        response = self.responses[self.calls - 1]
        return _FakeRequestContext(response)


class _TimeoutSession:
    def __init__(self):
        self.calls = 0

    def request(self, method, url, params=None, json=None, headers=None):
        self.calls += 1
        raise asyncio.TimeoutError()


class TestAsyncClientInit:
    def test_default_init(self):
        client = AsyncEventyayClient()
        assert "api.eventyay.com" in client.base_url
        assert client.api_key is None
        assert client.timeout == 30

    def test_with_api_key(self):
        client = AsyncEventyayClient(api_key="test-key")
        assert client.headers["Authorization"] == "Token test-key"

    def test_uses_jsonapi_headers(self):
        client = AsyncEventyayClient()
        assert client.headers["Content-Type"] == "application/vnd.api+json"
        assert client.headers["Accept"] == "application/vnd.api+json"

    def test_repr(self):
        client = AsyncEventyayClient(api_key="testkey1234")
        assert "test..." in repr(client)

    def test_no_key_repr(self):
        client = AsyncEventyayClient()
        assert "None" in repr(client)


class TestAsyncClientContextManager:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AsyncEventyayClient(api_key="test") as client:
            assert client._session is not None
        # After exit, session should be closed
        assert client._session is None


class TestAsyncClientConfig:
    def test_custom_timeout(self):
        client = AsyncEventyayClient(timeout=60)
        assert client.timeout == 60

    def test_custom_retries(self):
        client = AsyncEventyayClient(max_retries=5)
        assert client.max_retries == 5

    def test_custom_base_url(self):
        client = AsyncEventyayClient(base_url="https://custom.api.com/v2/")
        assert client.base_url == "https://custom.api.com/v2"


class TestAsyncClientJsonHandling:
    @pytest.mark.asyncio
    async def test_safe_json_raises_api_error_on_malformed_response(self):
        client = AsyncEventyayClient()
        response = AsyncMock()
        response.status = 200
        response.json.side_effect = ValueError("bad json")

        with pytest.raises(EventyayAPIError) as exc_info:
            await client._safe_json(response)

        assert exc_info.value.status_code == 200


class TestAsyncClientRetryPolicy:
    def test_retry_policy_does_not_regress_default_base_url(self):
        client = AsyncEventyayClient()
        assert client.base_url == "https://api.eventyay.com/v1"

    def test_get_event_attendees_resolves_to_attendees_mixin(self):
        assert AsyncEventyayClient.get_event_attendees is AsyncAttendeesMixin.get_event_attendees

    def test_get_event_access_codes_resolves_to_access_codes_mixin(self):
        assert AsyncEventyayClient.get_event_access_codes is AsyncAccessCodesMixin.get_event_access_codes

    def test_get_role_invites_resolves_to_role_invites_mixin(self):
        assert AsyncEventyayClient.get_role_invites is AsyncRoleInvitesMixin.get_role_invites

    def test_get_event_ticket_tags_resolves_to_ticket_tags_mixin(self):
        assert AsyncEventyayClient.get_event_ticket_tags is AsyncTicketTagsMixin.get_event_ticket_tags

    def test_get_event_types_resolves_to_event_types_mixin(self):
        assert AsyncEventyayClient.get_event_types is AsyncEventTypesMixin.get_event_types

    def test_get_event_topics_resolves_to_event_topics_mixin(self):
        assert AsyncEventyayClient.get_event_topics is AsyncEventTopicsMixin.get_event_topics

    def test_get_event_sub_topics_resolves_to_event_sub_topics_mixin(self):
        assert AsyncEventyayClient.get_event_sub_topics is AsyncEventSubTopicsMixin.get_event_sub_topics

    def test_get_notifications_resolves_to_notifications_mixin(self):
        assert AsyncEventyayClient.get_notifications is AsyncNotificationsMixin.get_notifications

    def test_get_pages_resolves_to_pages_mixin(self):
        assert AsyncEventyayClient.get_pages is AsyncPagesMixin.get_pages

    def test_get_services_resolves_to_services_mixin(self):
        assert AsyncEventyayClient.get_services is AsyncServicesMixin.get_services

    def test_get_activities_resolves_to_misc_resources_mixin(self):
        assert AsyncEventyayClient.get_activities is AsyncMiscResourcesMixin.get_activities

    def test_login_resolves_to_auth_mixin(self):
        assert AsyncEventyayClient.login is AsyncAuthMixin.login

    @pytest.mark.asyncio
    async def test_does_not_retry_post_on_server_error(self):
        client = AsyncEventyayClient(max_retries=3)
        session = _FakeSession([_FakeResponse(500, {"detail": "boom"}, "boom")])

        async def _fake_ensure_session():
            return session

        client._ensure_session = _fake_ensure_session

        with pytest.raises(EventyayAPIError):
            await client._post("events", json={"data": {}})

        assert session.calls == 1

    @pytest.mark.asyncio
    async def test_retries_get_on_server_error(self, monkeypatch):
        client = AsyncEventyayClient(max_retries=3)
        session = _FakeSession(
            [
                _FakeResponse(500, {"detail": "temporary"}, "temporary"),
                _FakeResponse(200, {"data": []}, "ok"),
            ]
        )

        async def _fake_ensure_session():
            return session

        client._ensure_session = _fake_ensure_session

        async def _no_sleep(_):
            return None

        monkeypatch.setattr(asyncio, "sleep", _no_sleep)

        result = await client._get("events")
        assert result == {"data": []}
        assert session.calls == 2

    @pytest.mark.asyncio
    async def test_does_not_retry_post_on_timeout(self):
        client = AsyncEventyayClient(max_retries=3)
        session = _TimeoutSession()

        async def _fake_ensure_session():
            return session

        client._ensure_session = _fake_ensure_session

        with pytest.raises(EventyayTimeoutError):
            await client._post("events", json={"data": {}})

        assert session.calls == 1

    @pytest.mark.asyncio
    async def test_retries_get_on_connection_error(self, monkeypatch):
        client = AsyncEventyayClient(max_retries=2)

        class _ClientErrorSession:
            def __init__(self):
                self.calls = 0

            def request(self, method, url, params=None, json=None, headers=None):
                self.calls += 1
                raise aiohttp.ClientError("network down")

        session = _ClientErrorSession()

        async def _fake_ensure_session():
            return session

        client._ensure_session = _fake_ensure_session

        async def _no_sleep(_):
            return None

        monkeypatch.setattr(asyncio, "sleep", _no_sleep)

        with pytest.raises(EventyayConnectionError):
            await client._get("events")

        assert session.calls == 3

    @pytest.mark.asyncio
    async def test_post_supports_idempotency_key(self):
        client = AsyncEventyayClient(max_retries=0)
        session = _FakeSession([_FakeResponse(200, {"data": {}})])

        async def _fake_ensure_session():
            return session

        client._ensure_session = _fake_ensure_session

        await client._post("events", json={"data": {}}, idempotency_key="idem-789")

        assert session.last_headers["Idempotency-Key"] == "idem-789"

    @pytest.mark.asyncio
    async def test_rejects_absolute_url_endpoints(self):
        client = AsyncEventyayClient(max_retries=0)

        with pytest.raises(EventyayValidationError):
            await client._get("https://evil.example/path")

    @pytest.mark.asyncio
    async def test_rejects_bidi_control_chars(self):
        client = AsyncEventyayClient(max_retries=0)

        with pytest.raises(EventyayValidationError):
            await client._get("events/\u202Eabc")
