# Eventyay Python SDK

A Python client library for the Eventyay API that simplifies interaction with event management endpoints.

## Overview

The Eventyay Python SDK provides a cleaner, more Pythonic way to interact with the Eventyay REST API. Instead of making raw HTTP requests, developers can use simple Python functions to manage organizers, events, and more.

## Installation

```bash
pip install eventyay
```

Or install from source:

```bash
git clone https://github.com/shivam-pawar-7217/eventyay-python-sdk.git
cd eventyay-python-sdk
pip install -e .
```

## Quick Start

```python
from eventyay import EventyayClient

# Initialize the client
client = EventyayClient(base_url="https://dev.eventyay.com/api/v1")

# With API authentication
client = EventyayClient(
    base_url="https://dev.eventyay.com/api/v1",
    api_key="your-api-key-here"
)

# Get organizers
organizers = client.get_organizers(page=1, page_size=10)
print(organizers)
```

## Features

- Clean, Pythonic API interface
- Built-in authentication support
- Comprehensive error handling
- Full type hints support
- Pagination support
- Well-documented methods

## Requirements

- Python 3.7+
- requests >= 2.28.0

## Documentation

For detailed documentation, see the [docs](docs/) directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Links

- **API Documentation**: https://dev.eventyay.com/api/v1
- **GitHub Repository**: https://github.com/shivam-pawar-7217/eventyay-python-sdk
- **Issue Tracker**: https://github.com/shivam-pawar-7217/eventyay-python-sdk/issues
