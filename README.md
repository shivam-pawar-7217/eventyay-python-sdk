# Eventyay Python SDK

A modern, type-safe, asynchronous Python client for the [Eventyay API](https://api.eventyay.com/).

## 🌟 Features

*   **16 Full API Domains**: Organizers, Events, Attendees, Speakers, Sessions, Tickets, Tracks, Microlocations, Sponsors, DiscountCodes, Orders, Tax, Users, Roles, Feedbacks, and Settings.
*   **Async & Sync**: Full support for both synchronous and asynchronous applications.
*   **Type Safety**: Returns Pydantic models for excellent IDE support and validation.
*   **Auto-Pagination**: Helper methods to fetch *all* results automatically.
*   **Reliability**: Built-in exponential backoff for rate limits and server errors.
*   **CLI Tool**: Includes a powerful command-line interface (`eventyay`).

## 📦 Installation

```bash
pip install eventyay
```

## 🖥️ CLI Usage

The SDK comes with a command-line tool `eventyay` to manage resources directly from your terminal.

```bash
# Check version
eventyay version

# List all events (Rich Table)
eventyay events list

# Show detailed event info (Rich Panel)
eventyay events show <id>

# List all organizers
eventyay organizers list

# Show organizer details
eventyay organizers show <id>
```

## 🚀 Quick Start (Python)

### Synchronous Usage

```python
from eventyay.client import EventyayClient

client = EventyayClient(api_key="YOUR_API_KEY")

# Fetch all events (Auto-paginated!)
events = client.get_all_events()
for event in events:
    print(f"{event.name} starts at {event.starts_at}")
```

### Asynchronous Usage

```python
import asyncio
from eventyay.async_client import AsyncEventyayClient

async def main():
    client = AsyncEventyayClient(api_key="YOUR_API_KEY")
    
    # Fetch data asynchronously
    events = await client.get_all_events()
    print(f"Fetched {len(events)} events")

asyncio.run(main())
```

### Handling Large Data (Pagination)

The SDK provides helper methods to automatically fetch **all** results from paginated endpoints.
These methods return a list of Pydantic objects (`Organizer`, `Event`).

```python
# Fetch ALL organizers (returns List[Organizer])
all_organizers = client.get_all_organizers()
for org in all_organizers:
    print(org.name) # Type-safe access!

# Fetch ALL events (returns List[Event])
all_events = client.get_all_events()
print(f"Total events fetched: {len(all_events)}")
```

### Reliability (Auto-Retries)

The client automatically retries requests that fail due to:
*   Rate Limits (HTTP 429)
*   Server Errors (HTTP 500, 502, 503, 504)

It uses exponential backoff to be a good API citizen.

## 🛡️ Type Safety (Pydantic Models)

The SDK now returns typed objects instead of raw dictionaries. This enables autocomplete and validation in your IDE.

```python
event = client.get_event(1)
# Before: print(event['name'])
# Now:
print(event.name)
print(event.starts_at)
```

## 🤝 Contributing

Contributions are highly welcome! Please feel free to submit a Pull Request

