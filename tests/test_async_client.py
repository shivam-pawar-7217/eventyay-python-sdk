"""Tests for the AsyncEventyayClient."""

from unittest.mock import AsyncMock

import pytest

from eventyay.async_client import AsyncEventyayClient
from eventyay.exceptions import EventyayAPIError


class TestAsyncClientInit:
    def test_default_init(self):
        client = AsyncEventyayClient()
        assert "dev.eventyay.com" in client.base_url
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
