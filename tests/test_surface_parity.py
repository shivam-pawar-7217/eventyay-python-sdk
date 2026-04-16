"""Guardrails for sync/async client public API surface parity."""

from eventyay.async_client import AsyncEventyayClient
from eventyay.client import EventyayClient


def _public_callables(cls) -> set[str]:
    names: set[str] = set()
    for name in dir(cls):
        if name.startswith("_"):
            continue
        attr = getattr(cls, name)
        if callable(attr):
            names.add(name)
    return names


def test_sync_async_public_surface_parity():
    sync_methods = _public_callables(EventyayClient)
    async_methods = _public_callables(AsyncEventyayClient)

    # Sync-only convenience methods that intentionally auto-paginate.
    allowed_sync_only = {
        "get_all_events",
        "get_all_organizers",
        "get_all_users",
    }

    sync_only = sync_methods - async_methods
    async_only = async_methods - sync_methods

    assert sync_only == allowed_sync_only
    assert async_only == set()
