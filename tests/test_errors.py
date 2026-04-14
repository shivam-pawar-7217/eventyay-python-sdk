"""Tests for error handling and exception mapping."""

from unittest.mock import Mock

import pytest
from requests.exceptions import ConnectionError, HTTPError, Timeout

from eventyay.client import EventyayClient
from eventyay.exceptions import (
    EventyayAPIError,
    EventyayAuthenticationError,
    EventyayConnectionError,
    EventyayNotFoundError,
    EventyayRateLimitError,
    EventyayTimeoutError,
    EventyayValidationError,
)


@pytest.fixture
def client():
    c = EventyayClient(api_key="test-key")
    c.session = Mock()
    return c


class TestErrorMapping:
    def test_401_raises_auth_error(self, client):
        response = Mock()
        response.status_code = 401
        response.json.return_value = {"detail": "Invalid token"}
        response.text = '{"detail": "Invalid token"}'
        response.raise_for_status.side_effect = HTTPError(response=response)
        client.session.get.return_value = response

        with pytest.raises(EventyayAuthenticationError) as exc_info:
            client._get("test")

        assert exc_info.value.status_code == 401

    def test_403_raises_auth_error(self, client):
        response = Mock()
        response.status_code = 403
        response.json.return_value = {"detail": "Forbidden"}
        response.text = '{"detail": "Forbidden"}'
        response.raise_for_status.side_effect = HTTPError(response=response)
        client.session.get.return_value = response

        with pytest.raises(EventyayAuthenticationError):
            client._get("test")

    def test_404_raises_not_found(self, client):
        response = Mock()
        response.status_code = 404
        response.json.return_value = {"detail": "Not found"}
        response.text = '{"detail": "Not found"}'
        response.raise_for_status.side_effect = HTTPError(response=response)
        client.session.get.return_value = response

        with pytest.raises(EventyayNotFoundError) as exc_info:
            client._get("events/999")

        assert exc_info.value.status_code == 404

    def test_429_raises_rate_limit(self, client):
        response = Mock()
        response.status_code = 429
        response.json.return_value = {"detail": "Too many requests"}
        response.text = '{"detail": "Too many requests"}'
        response.raise_for_status.side_effect = HTTPError(response=response)
        client.session.get.return_value = response

        with pytest.raises(EventyayRateLimitError) as exc_info:
            client._get("test")

        assert exc_info.value.status_code == 429

    def test_400_raises_validation_error(self, client):
        response = Mock()
        response.status_code = 400
        response.json.return_value = {"detail": "Bad request"}
        response.text = '{"detail": "Bad request"}'
        response.raise_for_status.side_effect = HTTPError(response=response)
        client.session.get.return_value = response

        with pytest.raises(EventyayValidationError):
            client._get("test")

    def test_500_raises_api_error(self, client):
        response = Mock()
        response.status_code = 500
        response.json.return_value = {"detail": "Internal server error"}
        response.text = '{"detail": "Internal server error"}'
        response.raise_for_status.side_effect = HTTPError(response=response)
        client.session.get.return_value = response

        with pytest.raises(EventyayAPIError) as exc_info:
            client._get("test")

        assert exc_info.value.status_code == 500

    def test_connection_error(self, client):
        client.session.get.side_effect = ConnectionError("No route to host")

        with pytest.raises(EventyayConnectionError):
            client._get("test")

    def test_timeout_error(self, client):
        client.session.get.side_effect = Timeout("Connection timed out")

        with pytest.raises(EventyayTimeoutError):
            client._get("test")

    def test_malformed_json_success_response_raises_api_error(self, client):
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("invalid json")
        client.session.get.return_value = response

        with pytest.raises(EventyayAPIError) as exc_info:
            client._get("test")

        assert exc_info.value.status_code == 200


class TestExceptionAttributes:
    def test_status_code_attribute(self):
        exc = EventyayNotFoundError(
            "Not found", status_code=404, response_body='{"detail":"Not found"}'
        )
        assert exc.status_code == 404
        assert exc.response_body == '{"detail":"Not found"}'

    def test_str_representation(self):
        exc = EventyayAPIError("Something broke", status_code=500)
        assert "[HTTP 500]" in str(exc)
        assert "Something broke" in str(exc)

    def test_base_exception_no_status(self):
        exc = EventyayAPIError("Generic error")
        assert exc.status_code is None
        assert str(exc) == "Generic error"

    def test_response_body_is_redacted(self):
        body = '{"token":"abc123","detail":"failed"}\nAuthorization: Bearer secret-token'
        exc = EventyayAPIError("Bad", status_code=400, response_body=body)
        assert "abc123" not in exc.response_body
        assert "secret-token" not in exc.response_body
        assert "[REDACTED]" in exc.response_body

    def test_response_body_is_truncated(self):
        body = "x" * 3000
        exc = EventyayAPIError("Bad", status_code=400, response_body=body)
        assert len(exc.response_body) == 2048
