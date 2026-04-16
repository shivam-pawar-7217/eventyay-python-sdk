"""Tests for JSON:API parsing utilities."""

import pytest

from eventyay.utils import (
    _convert_keys,
    build_jsonapi_payload,
    clean_dict,
    dasherized_to_snake,
    parse_jsonapi_list,
    parse_jsonapi_resource,
    parse_pagination_params,
    snake_to_dasherized,
)
from eventyay.exceptions import EventyayParsingError


class TestDasherizedToSnake:
    def test_basic(self):
        assert dasherized_to_snake("starts-at") == "starts_at"

    def test_multi_dash(self):
        assert dasherized_to_snake("is-sessions-speakers-enabled") == "is_sessions_speakers_enabled"

    def test_no_dash(self):
        assert dasherized_to_snake("name") == "name"


class TestSnakeToDasherized:
    def test_basic(self):
        assert snake_to_dasherized("starts_at") == "starts-at"

    def test_multi_underscore(self):
        assert snake_to_dasherized("is_sessions_speakers_enabled") == "is-sessions-speakers-enabled"


class TestConvertKeys:
    def test_converts_flat_dict(self):
        result = _convert_keys({"starts-at": "2026-01-01", "location-name": "Berlin"})
        assert result == {"starts_at": "2026-01-01", "location_name": "Berlin"}

    def test_converts_nested_dict(self):
        result = _convert_keys({"some-data": {"inner-key": "value"}})
        assert result == {"some_data": {"inner_key": "value"}}

    def test_handles_list_values(self):
        result = _convert_keys({"items": [{"item-name": "A"}, {"item-name": "B"}]})
        assert result == {"items": [{"item_name": "A"}, {"item_name": "B"}]}


class TestParseJsonapiResource:
    def test_parses_jsonapi_single_resource(self):
        response = {
            "data": {
                "type": "event",
                "id": "42",
                "attributes": {
                    "name": "FOSSASIA",
                    "starts-at": "2026-03-15T09:00:00Z",
                    "is-featured": True,
                    "location-name": "Singapore",
                },
            },
            "jsonapi": {"version": "1.0"},
        }

        result = parse_jsonapi_resource(response)

        assert result["id"] == 42
        assert result["name"] == "FOSSASIA"
        assert result["starts_at"] == "2026-03-15T09:00:00Z"
        assert result["is_featured"] is True
        assert result["location_name"] == "Singapore"

    def test_parses_plain_dict(self):
        """Backward compatibility for non-JSON:API responses."""
        response = {"id": 1, "name": "Test", "starts-at": "2026-01-01"}

        result = parse_jsonapi_resource(response)

        assert result["id"] == 1
        assert result["name"] == "Test"
        assert result["starts_at"] == "2026-01-01"

    def test_parses_data_wrapper_without_attributes(self):
        """Handles old-style {"data": {...}} responses."""
        response = {"data": {"id": 1, "name": "Test"}}

        result = parse_jsonapi_resource(response)

        assert result["id"] == 1
        assert result["name"] == "Test"

    def test_strict_mode_rejects_missing_attributes(self):
        response = {"data": {"id": 1, "name": "Test"}}

        with pytest.raises(EventyayParsingError):
            parse_jsonapi_resource(response, strict=True)


class TestParseJsonapiList:
    def test_parses_jsonapi_list_response(self):
        response = {
            "data": [
                {
                    "type": "event",
                    "id": "1",
                    "attributes": {
                        "name": "Event One",
                        "starts-at": "2026-01-01T00:00:00Z",
                    },
                },
                {
                    "type": "event",
                    "id": "2",
                    "attributes": {
                        "name": "Event Two",
                        "starts-at": "2026-06-01T00:00:00Z",
                    },
                },
            ],
            "links": {
                "self": "https://api.eventyay.com/v1/events?page[number]=1",
                "next": "https://api.eventyay.com/v1/events?page[number]=2",
            },
            "meta": {"count": 100},
            "jsonapi": {"version": "1.0"},
        }

        result = parse_jsonapi_list(response)

        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == 1
        assert result["data"][0]["name"] == "Event One"
        assert result["data"][0]["starts_at"] == "2026-01-01T00:00:00Z"
        assert result["data"][1]["id"] == 2
        assert result["links"]["next"] is not None
        assert result["meta"]["count"] == 100

    def test_parses_old_format_list(self):
        """Backward compatibility for non-JSON:API list responses."""
        response = {
            "data": [
                {"id": 1, "name": "Event One"},
                {"id": 2, "name": "Event Two"},
            ]
        }

        result = parse_jsonapi_list(response)

        assert len(result["data"]) == 2
        assert result["data"][0]["name"] == "Event One"

    def test_strict_mode_rejects_items_without_attributes(self):
        response = {"data": [{"id": 1, "name": "Event One"}]}

        with pytest.raises(EventyayParsingError):
            parse_jsonapi_list(response, strict=True)


class TestBuildJsonapiPayload:
    def test_builds_create_payload(self):
        payload = build_jsonapi_payload(
            "event",
            {"name": "My Event", "starts_at": "2026-01-01T00:00:00Z", "timezone": "UTC"},
        )

        assert payload["data"]["type"] == "event"
        assert payload["data"]["attributes"]["name"] == "My Event"
        assert payload["data"]["attributes"]["starts-at"] == "2026-01-01T00:00:00Z"
        assert "id" not in payload["data"]

    def test_builds_update_payload(self):
        payload = build_jsonapi_payload(
            "event",
            {"name": "Updated Event"},
            resource_id="42",
        )

        assert payload["data"]["type"] == "event"
        assert payload["data"]["id"] == "42"
        assert payload["data"]["attributes"]["name"] == "Updated Event"

    def test_skips_none_values(self):
        payload = build_jsonapi_payload(
            "event",
            {"name": "Event", "description": None},
        )

        assert "description" not in payload["data"]["attributes"]


class TestParsePaginationParams:
    def test_parses_jsonapi_pagination(self):
        url = "https://api.eventyay.com/v1/events?page[number]=3&page[size]=25"
        result = parse_pagination_params(url)
        assert result["page[number]"] == "3"
        assert result["page[size]"] == "25"

    def test_parses_simple_pagination(self):
        url = "https://api.eventyay.com/v1/events?page=3&page_size=25"
        result = parse_pagination_params(url)
        assert result["page"] == "3"
        assert result["page_size"] == "25"

    def test_empty_url(self):
        result = parse_pagination_params("https://api.eventyay.com/v1/events")
        assert result == {}


class TestCleanDict:
    def test_removes_none_values(self):
        result = clean_dict({"a": 1, "b": None, "c": "hello", "d": None})
        assert result == {"a": 1, "c": "hello"}

    def test_keeps_falsy_non_none(self):
        result = clean_dict({"a": 0, "b": "", "c": False, "d": None})
        assert result == {"a": 0, "b": "", "c": False}
