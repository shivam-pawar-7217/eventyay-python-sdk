# Contributing to Eventyay Python SDK

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shivam-pawar-7217/eventyay-python-sdk.git
   cd eventyay-python-sdk
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Install with dev dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We use [Black](https://github.com/psf/black) for code formatting and [isort](https://github.com/PyCQA/isort) for import sorting.

```bash
# Format code
black eventyay/ tests/

# Sort imports
isort eventyay/ tests/

# Lint
flake8 eventyay/ tests/ --max-line-length=127
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=eventyay --cov-report=term-missing

# Run a specific test file
pytest tests/test_events.py -v

# Run a specific test
pytest tests/test_events.py::TestGetEvent::test_returns_event_model -v
```

## Project Structure

```
eventyay-python-sdk/
├── eventyay/                # Main package
│   ├── __init__.py          # Package exports
│   ├── client.py            # Synchronous API client
│   ├── async_client.py      # Asynchronous API client
│   ├── models.py            # Pydantic data models (16 resources)
│   ├── exceptions.py        # Typed exception hierarchy
│   ├── cli.py               # Typer CLI application
│   ├── utils.py             # Shared utilities
│   ├── organizers.py        # OrganizersMixin
│   ├── events.py            # EventsMixin
│   ├── tickets.py           # TicketsMixin
│   ├── attendees.py         # AttendeesMixin
│   ├── speakers.py          # SpeakersMixin
│   ├── sessions.py          # SessionsMixin
│   ├── tracks.py            # TracksMixin
│   ├── microlocations.py    # MicrolocationsMixin
│   ├── sponsors.py          # SponsorsMixin
│   ├── discount_codes.py    # DiscountCodesMixin
│   ├── orders.py            # OrdersMixin
│   ├── tax.py               # TaxMixin
│   ├── users.py             # UsersMixin
│   ├── roles.py             # RolesMixin
│   ├── feedbacks.py         # FeedbacksMixin
│   ├── settings.py          # SettingsMixin
│   └── async_mixins.py      # All async mixin classes
├── tests/                   # Test suite
├── docs/                    # Sphinx documentation
├── examples/                # Usage examples
├── setup.py                 # Package configuration
├── pyproject.toml           # Tool configuration
├── requirements.txt         # Runtime dependencies
├── CHANGELOG.md             # Release history
└── CONTRIBUTING.md          # This file
```

## Architecture

The SDK uses a **Client + Mixin** pattern:

- `EventyayClient` (sync) and `AsyncEventyayClient` (async) are the main entry points.
- Each API domain (Events, Organizers, etc.) is implemented as a **Mixin class**.
- Both clients inherit from all relevant mixins using multiple inheritance.
- All API responses are parsed into **Pydantic models** for type safety.
- HTTP errors are mapped to a **typed exception hierarchy**.

## Pull Request Guidelines

1. **One feature per PR**: Keep PRs focused and reviewable.
2. **Write tests**: All new features must have corresponding tests.
3. **Follow the code style**: Run `black` and `isort` before committing.
4. **Update CHANGELOG**: Add your changes under `[Unreleased]`.
5. **Add docstrings**: All public methods must have docstrings.
6. **No breaking changes**: Unless discussed and approved first.

## Reporting Issues

- Use [GitHub Issues](https://github.com/shivam-pawar-7217/eventyay-python-sdk/issues)
- Include your Python version, SDK version, and a minimal reproduction case.
