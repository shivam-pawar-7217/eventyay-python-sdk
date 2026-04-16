Quickstart Guide
================

Synchronous Usage
-----------------

.. code-block:: python

   from eventyay import EventyayClient

   # Initialize client
   client = EventyayClient(api_key="your_token")

   # Get a list of events
   events = client.get_events()
   for event in events.data:
       print(f"Event: {event.name}")

Asynchronous Usage
------------------

.. code-block:: python

   import asyncio
   from eventyay import AsyncEventyayClient

   async def main():
       async with AsyncEventyayClient(api_key="your_token") as client:
           events = await client.get_events()
           for event in events.data:
               print(f"Async Event: {event.name}")

   asyncio.run(main())

Strict JSON:API Mode
--------------------

.. code-block:: python

   from eventyay import EventyayClient

   # strict_jsonapi=True raises parsing errors on malformed wrappers
   client = EventyayClient(api_key="your_token", strict_jsonapi=True)
   events = client.get_events()

Idempotency Keys For Writes
---------------------------

.. code-block:: python

   new_event = client.create_event(
       name="DevConf 2026",
       identifier="devconf-2026",
       starts_at="2026-12-01T09:00:00Z",
       ends_at="2026-12-01T17:00:00Z",
       timezone="UTC",
       idempotency_key="devconf-create-2026",
   )

Creating an Event
-----------------

.. code-block:: python

   new_event = client.create_event(
       name="DevConf 2026",
       identifier="devconf-2026",
       starts_at="2026-12-01T09:00:00Z",
       ends_at="2026-12-01T17:00:00Z",
       timezone="UTC"
   )
   print(f"Created Event ID: {new_event.id}")
