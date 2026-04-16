# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Endpoint path validation in transport utilities to block absolute-URL injection attempts, bidi control characters, and unsafe control bytes.
- Strict JSON:API parsing mode with typed parsing failures via `EventyayParsingError`.
- Idempotency-key support for write operations across sync and async clients.
- Additional typed API domains and helpers: access codes, role invites, ticket tags, event types, event topics, event sub topics, notifications, pages, services, auth operations, and operational copy/upload helpers.
- Broader read/list helper coverage via misc resource endpoints.
- Optional live contract test workflow and production hardening documentation.

### Changed
- Default async base URL aligned to `https://api.eventyay.com/v1`.
- Retry behavior hardened to avoid retries for mutating async methods while preserving retries for safe methods.
- Mixins now use transport base contracts for stronger static typing and clearer architecture.
- CI now includes bidi control scanning and mypy type checks.

### Security
- Bidirectional Unicode control scanning upgraded and enforced as a CI gate.
- Endpoint composition now validates relative path safety before requests are dispatched.

## [0.1.0] - 2026-04-10

### Added
- **16 API domains**: Organizers, Events, Attendees, Speakers, Sessions, Tickets, Tracks, Microlocations, Sponsors, DiscountCodes, Orders, Tax, Users, Roles, Feedbacks, Settings.
- **Synchronous client** (`EventyayClient`) with requests-based HTTP transport, configurable timeout, and automatic retries with exponential backoff.
- **Asynchronous client** (`AsyncEventyayClient`) with aiohttp-based HTTP transport, retry logic, and full error mapping.
- **Pydantic models** for all 16 resource types with type-safe attribute access and `extra="ignore"` for forward compatibility.
- **Paginated list wrappers** (`EventList`, `OrganizerList`, etc.) with `data`, `links`, and `meta` fields.
- **Auto-pagination helpers** (`get_all_events()`, `get_all_organizers()`, `get_all_users()`) to exhaust all pages.
- **CRUD operations** for Events and Organizers (create, update, delete).
- **User management**: list, get, update users with admin-level JSON:API payloads.
- **Typed exception hierarchy**: `EventyayAPIError` → `EventyayAuthenticationError`, `EventyayNotFoundError`, `EventyayValidationError`, `EventyayConnectionError`, `EventyayTimeoutError`, `EventyayRateLimitError`. All carry `status_code` and `response_body` attributes.
- **CLI tool** (`eventyay`) built with Typer and Rich:
  - `login` / `logout` / `config` for authentication management.
  - `events list|show|create|update|delete` with full CRUD.
  - `organizers list|show|create|update|delete` with full CRUD.
  - Read-only `list` and `show` for all 14 remaining domains.
  - `--output json` flag for machine-readable output on every command.
  - `version` command.
- **Context manager support** for both sync and async clients.
- **PEP 561** `py.typed` marker for type checker compatibility.
- **CI/CD** via GitHub Actions: lint (flake8), test (pytest + coverage), import smoke test across Python 3.9–3.12.
- **Comprehensive test suite**: 80+ tests covering all domains, error mapping, CLI commands, pagination utilities, and client configuration.
- **Documentation**: README with badges, CLI reference, code examples, development guide.
