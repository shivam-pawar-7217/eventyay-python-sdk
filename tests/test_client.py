"""Tests for the synchronous EventyayClient."""

from eventyay.client import EventyayClient


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
