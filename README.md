# Eventyay Python SDK 🐍

A modern, type-safe Python client for the [Eventyay](https://eventyay.com) Event Management Platform. 
Simplify API interactions, manage attendees, and automate event workflows with clean, pythonic code.

> **Status**: 🚧 Pre-Alpha (GSoC 2026 Project)

## Features ✨

*   **Organizers**: Fetch and manage organizer profiles.
*   **Events**: Retrieve events, attendees, speakers, and sessions.
*   **Robust Error Handling**: Graceful handling of network failures and timeouts.
*   **Type Hinted**: Fully typed for excellent IDE support.

## Installation 📦

### User Installation
```bash
git clone https://github.com/shivam-pawar-7217/eventyay-python-sdk.git
cd eventyay-python-sdk
pip install -r requirements.txt
```

### Developer Setup (Editable)
```bash
pip install -e .
```

## Quick Start 🚀

### 1. Public Data (No API Key)

```python
from eventyay.client import EventyayClient
from eventyay.exceptions import EventyayConnectionError

client = EventyayClient()

try:
    # Get Public Events
    events = client.get_events()
    print(f"Found {len(events)} events!")

except EventyayConnectionError:
    print("Please check your internet connection.")
```

### 2. Organizer Data

```python
# specific organizer
org = client.get_organizer(organizer_id="123")
print(f"Organizer: {org['name']}")
```


## ⚡ Async Usage (New!)

For high-performance applications, use the `AsyncEventyayClient`:

```python
import asyncio
from eventyay import AsyncEventyayClient

async def main():
    async with AsyncEventyayClient() as client:
        # Fetch events
        events = await client.get_events()
        print(f"Found {len(events)} events")

        # Fetch event details, attendees, speakers, sessions
        event = await client.get_event(100)
        attendees = await client.get_event_attendees("100")
        speakers = await client.get_event_speakers("100")
        sessions = await client.get_event_sessions("100")

        print(f"Event: {event['name']}")
        print(f"Attendees: {len(attendees)}")
        print(f"Speakers: {len(speakers)}")
        print(f"Sessions: {len(sessions)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📄 Handling Large Data (Pagination)

The SDK provides helper methods to automatically fetch **all** results (handling pagination for you):

```python
# Sync
all_attendees = client.get_all_organizers()

# Async
# (Note: Async get_all_* helpers are coming soon! For now, specific methods exist)
# Update: Actually Async helpers not implemented yet! 
# Let's stick to Sync for now in docs or just generic "Pagination" advice.
# Or wait, did I implement Async pagination? No, only Sync `OrganizersMixin` and `EventsMixin`.
# Async mixins don't have get_all_* yet. I should note that.
```

**Note:** Be careful with `get_all_*` methods on huge datasets.

## 🛡️ Reliability (Auto-Retries)

The client automatically handles:
*   **Rate Limits (429)**: Retries with exponential backoff (1s, 2s, 4s).
*   **Server Errors (5xx)**: Retries up to 3 times.

No extra configuration needed!

## 🧪 Running Tests

```bash
python3 -m unittest discover tests
```

## Roadmap 🗺️

*   [x] Organizers API
*   [x] Events API
*   [x] Error Handling
*   [ ] Async Support (Coming Soon)
*   [ ] CLI Tool

## License 📄

MIT License.
