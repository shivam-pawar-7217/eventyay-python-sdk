Production Hardening Guide
==========================

This guide outlines recommended settings and workflows for running the Eventyay SDK
in production services.

Strict JSON:API Mode
--------------------

Enable strict parsing to fail fast when upstream payload wrappers drift:

.. code-block:: python

   from eventyay import EventyayClient

   client = EventyayClient(
       api_key="YOUR_API_KEY",
       strict_jsonapi=True,
   )

Idempotency Keys For Writes
---------------------------

Write operations accept ``idempotency_key`` to reduce duplicate mutation risk:

.. code-block:: python

   event = client.create_event(
       name="FOSSASIA Summit",
       identifier="fossasia-summit-2026",
       starts_at="2026-04-01T09:00:00Z",
       ends_at="2026-04-01T18:00:00Z",
       timezone="UTC",
       idempotency_key="event-create-2026-04-01",
   )

Retry Policy
------------

The SDK retries only safe methods (``GET``, ``HEAD``, ``OPTIONS``) on transient
status and transport failures. Mutating methods fail fast to avoid duplicate writes.

Timeout and Session Lifecycle
-----------------------------

For async usage, prefer context-manager lifecycle management:

.. code-block:: python

   import asyncio
   from eventyay import AsyncEventyayClient

   async def main():
       async with AsyncEventyayClient(api_key="YOUR_API_KEY", timeout=30) as client:
           await client.get_events()

   asyncio.run(main())

Optional Live Contract Checks
-----------------------------

Run optional live checks against a deployed Eventyay API:

.. code-block:: bash

   EVENTYAY_LIVE_TEST=1 pytest tests/test_contract_live_optional.py -q

Environment variables:

* ``EVENTYAY_LIVE_BASE_URL`` (default: ``https://api.eventyay.com/v1``)
* ``EVENTYAY_LIVE_API_KEY`` (optional; required for protected endpoints)
