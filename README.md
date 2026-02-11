# Eventyay Python SDK 

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

## Running Tests 🧪

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
