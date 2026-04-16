"""Contract-style tests for representative JSON:API payload behavior.

These tests encode Eventyay-compatible payload shapes to protect parser
stability for maintainers across refactors.
"""

import pytest

from eventyay.exceptions import EventyayParsingError
from eventyay.utils import parse_jsonapi_list, parse_jsonapi_resource


def test_contract_event_resource_parsing():
    payload = {
        "data": {
            "type": "event",
            "id": "101",
            "attributes": {
                "name": "FOSSASIA Summit",
                "starts-at": "2026-04-01T09:00:00Z",
                "is-featured": True,
            },
        }
    }

    parsed = parse_jsonapi_resource(payload, strict=True)

    assert parsed["id"] == 101
    assert parsed["name"] == "FOSSASIA Summit"
    assert parsed["starts_at"] == "2026-04-01T09:00:00Z"
    assert parsed["is_featured"] is True


def test_contract_event_list_parsing():
    payload = {
        "data": [
            {
                "type": "event",
                "id": "101",
                "attributes": {"name": "FOSSASIA Summit"},
            },
            {
                "type": "event",
                "id": "102",
                "attributes": {"name": "OpenTech Meetup"},
            },
        ],
        "meta": {"count": 2},
    }

    parsed = parse_jsonapi_list(payload, strict=True)

    assert len(parsed["data"]) == 2
    assert parsed["data"][0]["id"] == 101
    assert parsed["data"][1]["id"] == 102
    assert parsed["meta"]["count"] == 2


def test_contract_strict_mode_rejects_broken_resource_wrapper():
    payload = {"data": {"id": "101", "name": "Broken"}}

    with pytest.raises(EventyayParsingError):
        parse_jsonapi_resource(payload, strict=True)


def test_contract_strict_mode_rejects_broken_list_wrapper():
    payload = {"data": [{"id": "101", "name": "Broken"}]}

    with pytest.raises(EventyayParsingError):
        parse_jsonapi_list(payload, strict=True)
