# Eventyay Python SDK

[![CI](https://github.com/shivam-pawar-7217/eventyay-python-sdk/actions/workflows/python-app.yml/badge.svg)](https://github.com/shivam-pawar-7217/eventyay-python-sdk/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, type-safe, asynchronous Python client for the [Eventyay API](https://api.eventyay.com/).

## 🌟 Features

*   **Core + Extended API Domain Coverage**: Full core domains plus additional typed helpers for access codes, role invites, ticket tags, event taxonomy resources, notifications, pages, services, and operational/auth flows.
*   **Async & Sync**: Full support for both synchronous and asynchronous applications.
*   **Type Safety**: Returns Pydantic models for excellent IDE support and validation.
*   **Auto-Pagination**: Helper methods to fetch *all* results automatically.
*   **Reliability**: Built-in exponential backoff for rate limits and server errors.
*   **Strict Mode (Optional)**: Enforce strict JSON:API wrappers for teams that prefer fail-fast contracts.
*   **Idempotency Support**: Write operations accept idempotency keys to reduce duplicate mutation risk.
*   **CLI Tool**: Includes a powerful command-line interface (`eventyay`) with rich output.
*   **Error Handling**: Typed exceptions with HTTP status codes and response bodies.

## 📦 Installation

```bash
pip install eventyay
```

For development:
```bash
pip install eventyay[dev]
```

## 🖥️ CLI Usage

The SDK comes with a command-line tool `eventyay` to manage resources directly from your terminal.

### Authentication

```bash
# Save API key to config
eventyay login

# View current configuration
eventyay config

# Remove stored API key
eventyay logout
```

You can also set the `EVENTYAY_API_KEY` environment variable.

### Events

```bash
# List all events (Rich Table)
eventyay events list

# List events as JSON (machine-readable)
eventyay events list --output json

# Show detailed event info (Rich Panel)
eventyay events show <id>

# Create a new event
eventyay events create --name "My Event" --identifier "my-event" \
    --starts-at "2026-01-01T09:00:00Z" --ends-at "2026-01-02T18:00:00Z" \
    --timezone UTC

# Update an event
eventyay events update <id> --name "Updated Name"

# Delete an event
eventyay events delete <id>
```

### All Supported Resources

```bash
# Organizers (CRUD)
eventyay organizers list|show|create|update|delete

# Event sub-resources (read-only)
eventyay speakers list <event_id>
eventyay sessions list <event_id>
eventyay tickets list <event_id>
eventyay attendees list <event_id>
eventyay tracks list <event_id>
eventyay microlocations list <event_id>
eventyay sponsors list <event_id>
eventyay discount-codes list <event_id>
eventyay orders list <event_id>
eventyay tax show <event_id>

# Platform-level resources
eventyay users list
eventyay roles list <event_id>
eventyay feedbacks list <event_id>
eventyay settings list
```

All `list` and `show` commands support `--output json` for machine-readable output.

## 🚀 Quick Start (Python)

### Synchronous Usage

```python
from eventyay import EventyayClient

client = EventyayClient(api_key="YOUR_API_KEY")

# Fetch all events (Auto-paginated!)
events = client.get_all_events()
for event in events:
    print(f"{event.name} starts at {event.starts_at}")
```

### Asynchronous Usage

```python
import asyncio
from eventyay import AsyncEventyayClient

async def main():
    async with AsyncEventyayClient(api_key="YOUR_API_KEY") as client:
        events = await client.get_events()
        print(f"Fetched {len(events.data)} events")

asyncio.run(main())
```

### Context Manager (Sync)

```python
with EventyayClient(api_key="YOUR_API_KEY") as client:
    organizers = client.get_all_organizers()
    for org in organizers:
        print(org.name)
```

### Handling Large Data (Pagination)

The SDK provides helper methods to automatically fetch **all** results from paginated endpoints.
These methods return a list of Pydantic objects (`Organizer`, `Event`).

```python
# Fetch ALL organizers (returns List[Organizer])
all_organizers = client.get_all_organizers()
for org in all_organizers:
    print(org.name)  # Type-safe access!

# Fetch ALL events (returns List[Event])
all_events = client.get_all_events()
print(f"Total events fetched: {len(all_events)}")
```

### Reliability (Auto-Retries)

The client automatically retries requests that fail due to:
*   Rate Limits (HTTP 429)
*   Server Errors (HTTP 500, 502, 503, 504)

It uses exponential backoff to be a good API citizen.

### Strict JSON:API Mode (Optional)

Set `strict_jsonapi=True` to enforce JSON:API resource/list wrappers strictly. This is
useful for CI and production environments that want fail-fast behavior on malformed
payloads.

```python
from eventyay import EventyayClient

client = EventyayClient(api_key="YOUR_API_KEY", strict_jsonapi=True)
events = client.get_events()
```

### Idempotency Keys For Writes

Mutating operations support `idempotency_key` so API gateways and backend services can
deduplicate retries safely.

```python
event = client.create_event(
    name="FOSSASIA Summit",
    identifier="fossasia-summit-2026",
    starts_at="2026-04-01T09:00:00Z",
    ends_at="2026-04-01T18:00:00Z",
    timezone="UTC",
    idempotency_key="evt-create-2026-04-01",
)
```

### Error Handling

```python
from eventyay import EventyayClient
from eventyay.exceptions import EventyayNotFoundError, EventyayAuthenticationError

client = EventyayClient(api_key="YOUR_API_KEY")

try:
    event = client.get_event(999)
except EventyayNotFoundError as e:
    print(f"Event not found (HTTP {e.status_code})")
except EventyayAuthenticationError as e:
    print(f"Bad credentials: {e}")
```

## 🛡️ Type Safety (Pydantic Models)

The SDK returns typed objects instead of raw dictionaries. This enables autocomplete and validation in your IDE.

```python
event = client.get_event(1)
print(event.name)        # str
print(event.starts_at)   # Optional[str]
print(event.online)      # bool
```

Core model types are importable from the top level:

```python
from eventyay import Event, Organizer, Attendee, Speaker, Session, Ticket
```

## 🔧 Development

### Setup

```bash
git clone https://github.com/shivam-pawar-7217/eventyay-python-sdk.git
cd eventyay-python-sdk
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v --cov=eventyay
```

### Code Style

```bash
black eventyay/ tests/
isort eventyay/ tests/
flake8 eventyay/ tests/
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.
