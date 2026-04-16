"""Optional live contract checks against a real Eventyay API deployment.

These tests are skipped by default and can be enabled in CI or local runs with:

    EVENTYAY_LIVE_TEST=1 pytest tests/test_contract_live_optional.py -q
"""

import os

import pytest

from eventyay import EventyayClient


RUN_LIVE = os.getenv("EVENTYAY_LIVE_TEST") == "1"


@pytest.mark.skipif(not RUN_LIVE, reason="Set EVENTYAY_LIVE_TEST=1 to run live contract checks")
def test_live_public_events_contract_shape():
    base_url = os.getenv("EVENTYAY_LIVE_BASE_URL", "https://api.eventyay.com/v1")
    api_key = os.getenv("EVENTYAY_LIVE_API_KEY")

    client = EventyayClient(
        base_url=base_url,
        api_key=api_key,
        strict_jsonapi=True,
        timeout=30,
    )

    events = client.get_events(page=1, page_size=2)

    # Contract assertions: parseable, list-shaped response with stable metadata wrappers.
    assert isinstance(events.data, list)
    if events.links is not None:
        assert isinstance(events.links, dict)
    if events.meta is not None:
        assert isinstance(events.meta, dict)


@pytest.mark.skipif(not RUN_LIVE, reason="Set EVENTYAY_LIVE_TEST=1 to run live contract checks")
@pytest.mark.parametrize(
    "method_name",
    [
        "get_event_locations",
        "get_video_streams",
        "get_groups",
        "get_custom_placeholders",
        "get_custom_system_roles",
    ],
)
def test_live_misc_public_methods_contract_shape(method_name: str):
    base_url = os.getenv("EVENTYAY_LIVE_BASE_URL", "https://api.eventyay.com/v1")
    api_key = os.getenv("EVENTYAY_LIVE_API_KEY")

    client = EventyayClient(
        base_url=base_url,
        api_key=api_key,
        strict_jsonapi=True,
        timeout=30,
    )

    method = getattr(client, method_name)
    resources = method(page=1, page_size=2)

    assert isinstance(resources.data, list)
    if resources.links is not None:
        assert isinstance(resources.links, dict)
    if resources.meta is not None:
        assert isinstance(resources.meta, dict)
