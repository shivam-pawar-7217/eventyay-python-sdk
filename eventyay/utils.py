"""
Eventyay SDK Utilities

Helper functions for API response parsing, pagination, and data transformation.
Includes JSON:API specification support for dasherized field name conversion.
"""

from typing import Any, Dict, Optional, cast
from urllib.parse import parse_qs, urlparse

from .exceptions import EventyayParsingError, EventyayValidationError


BIDI_CONTROL_CHARS = frozenset(
    {
        "\u202A",  # LRE
        "\u202B",  # RLE
        "\u202D",  # LRO
        "\u202E",  # RLO
        "\u2066",  # LRI
        "\u2067",  # RLI
        "\u2068",  # FSI
        "\u202C",  # PDF
        "\u2069",  # PDI
    }
)


def dasherized_to_snake(key: str) -> str:
    """
    Convert a dasherized key to snake_case.

    The Eventyay API (JSON:API spec with Flask-REST-JSONAPI) returns
    field names in dasherized format (e.g. 'starts-at', 'location-name').
    Our Pydantic models use snake_case ('starts_at', 'location_name').

    Args:
        key: A dasherized string like 'is-featured' or 'starts-at'.

    Returns:
        Snake-cased string like 'is_featured' or 'starts_at'.
    """
    return key.replace("-", "_")


def snake_to_dasherized(key: str) -> str:
    """
    Convert a snake_case key to dasherized format for JSON:API requests.

    Args:
        key: A snake_case string like 'starts_at' or 'location_name'.

    Returns:
        Dasherized string like 'starts-at' or 'location-name'.
    """
    return key.replace("_", "-")


def parse_jsonapi_resource(response_data: Dict[str, Any], strict: bool = False) -> Dict[str, Any]:
    """
    Parse a single JSON:API resource into a flat dictionary.

    JSON:API format:
    ```json
    {
      "data": {
        "type": "event",
        "id": "1",
        "attributes": {
          "name": "FOSSASIA",
          "starts-at": "2026-01-01T00:00:00Z"
        },
        "relationships": {...}
      }
    }
    ```

    Returns a flat dict with snake_case keys:
    ```python
    {"id": 1, "name": "FOSSASIA", "starts_at": "2026-01-01T00:00:00Z"}
    ```

    Also handles non-JSON:API responses (plain dicts) for backward compatibility.

    Args:
        response_data: The raw API response dictionary.

    Returns:
        A flat dictionary with snake_case keys ready for Pydantic model construction.
    """
    if not isinstance(response_data, dict):
        if strict:
            raise EventyayParsingError("Expected top-level response object to be a dictionary.")
        return cast(Dict[str, Any], response_data)

    parsed = _try_parse_resource_wrapper(response_data, strict)
    if parsed is not None:
        return parsed

    if "data" in response_data and strict:
        raise EventyayParsingError("Strict JSON:API mode expects 'data' to be a resource object.")

    if strict:
        raise EventyayParsingError("Strict JSON:API mode requires a top-level 'data' wrapper.")

    # Plain dict response (no 'data' wrapper) — backward compatible
    return cast(Dict[str, Any], _convert_keys(response_data))


def parse_jsonapi_list(response_data: Dict[str, Any], strict: bool = False) -> Dict[str, Any]:
    """
    Parse a JSON:API list response into a format compatible with our List models.

    JSON:API list format:
    ```json
    {
      "data": [
        {"type": "event", "id": "1", "attributes": {"name": "Evt1", ...}},
        {"type": "event", "id": "2", "attributes": {"name": "Evt2", ...}}
      ],
      "links": {"self": "...", "next": "...", "prev": "..."},
      "meta": {"count": 100},
      "jsonapi": {"version": "1.0"}
    }
    ```

    Returns:
    ```python
    {
      "data": [{"id": 1, "name": "Evt1"}, {"id": 2, "name": "Evt2"}],
      "links": {...},
      "meta": {...}
    }
    ```

    Args:
        response_data: The raw API response dictionary.

    Returns:
        A dictionary with 'data' (list of flat dicts), 'links', and 'meta'.
    """
    if not isinstance(response_data, dict):
        if strict:
            raise EventyayParsingError("Expected top-level list response object to be a dictionary.")
        return cast(Dict[str, Any], response_data)

    if "data" not in response_data:
        if strict:
            raise EventyayParsingError("Strict JSON:API mode requires a top-level 'data' wrapper.")
        return cast(Dict[str, Any], response_data)

    data = response_data["data"]

    # If data is a list, parse each item
    if isinstance(data, list):
        parsed_items: list[Any] = [_parse_jsonapi_list_item(item, strict) for item in data]

        result: Dict[str, Any] = {"data": parsed_items}

        # Preserve pagination links and meta
        if "links" in response_data:
            result["links"] = response_data["links"]
        if "meta" in response_data:
            result["meta"] = response_data["meta"]

        return result

    # data is a single resource (not a list) — shouldn't happen for list endpoints
    # but handle gracefully
    if strict:
        raise EventyayParsingError("Strict JSON:API mode requires 'data' to be a list response.")
    return cast(Dict[str, Any], response_data)


def _try_parse_resource_wrapper(
    response_data: Dict[str, Any], strict: bool
) -> Optional[Dict[str, Any]]:
    """Return parsed resource when a JSON:API-style data wrapper exists, otherwise None."""
    if "data" not in response_data or not isinstance(response_data["data"], dict):
        return None

    data = response_data["data"]
    if "attributes" in data:
        attributes = data["attributes"]
        if strict and not isinstance(attributes, dict):
            raise EventyayParsingError("Expected JSON:API resource 'attributes' to be an object.")

        flat = _convert_keys(attributes if isinstance(attributes, dict) else {})
        if "id" in data:
            flat["id"] = _coerce_resource_id(data["id"])
        return flat

    if strict:
        raise EventyayParsingError("Strict JSON:API mode requires 'data.attributes' in resource responses.")
    return _convert_keys(data)


def _parse_jsonapi_list_item(item: Any, strict: bool) -> Any:
    """Parse one list item according to JSON:API semantics."""
    if isinstance(item, dict) and "attributes" in item:
        attributes = item["attributes"]
        if strict and not isinstance(attributes, dict):
            raise EventyayParsingError(
                "Expected JSON:API resource 'attributes' to be an object in list response."
            )

        flat = _convert_keys(attributes if isinstance(attributes, dict) else {})
        if "id" in item:
            flat["id"] = _coerce_resource_id(item["id"])
        return flat

    if strict:
        raise EventyayParsingError(
            "Strict JSON:API mode requires each list item to include 'attributes'."
        )
    return _convert_keys(item) if isinstance(item, dict) else item


def _coerce_resource_id(value: Any) -> Any:
    """Coerce JSON:API IDs to int when possible while preserving original values on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def _convert_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively convert all dictionary keys from dasherized to snake_case.

    Args:
        data: Dictionary with potentially dasherized keys.

    Returns:
        Dictionary with snake_case keys.
    """
    if not isinstance(data, dict):
        return data

    result: Dict[str, Any] = {}
    for key, value in data.items():
        snake_key = dasherized_to_snake(key)
        if isinstance(value, dict):
            result[snake_key] = _convert_keys(value)
        elif isinstance(value, list):
            result[snake_key] = [
                _convert_keys(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            result[snake_key] = value
    return result


def build_jsonapi_payload(
    resource_type: str,
    attributes: Dict[str, Any],
    resource_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build a JSON:API compliant request payload.

    The Eventyay API expects request bodies in JSON:API format:
    ```json
    {
      "data": {
        "type": "event",
        "attributes": {
          "name": "My Event",
          "starts-at": "2026-01-01T00:00:00Z"
        }
      }
    }
    ```

    Args:
        resource_type: The JSON:API resource type (e.g. 'event', 'speaker').
        attributes: Dictionary of attributes in snake_case.
        resource_id: Optional resource ID (for PATCH requests).

    Returns:
        A JSON:API compliant request body dictionary.
    """
    # Convert snake_case keys to dasherized for the API
    dasherized_attrs = {}
    for key, value in attributes.items():
        if value is not None:
            dasherized_attrs[snake_to_dasherized(key)] = value

    payload: Dict[str, Any] = {
        "data": {
            "type": resource_type,
            "attributes": dasherized_attrs,
        }
    }

    if resource_id is not None:
        payload["data"]["id"] = str(resource_id)

    return payload


def parse_pagination_params(url: str) -> Dict[str, Any]:
    """
    Extract pagination parameters from a URL.

    Handles both JSON:API style (`page[number]`, `page[size]`)
    and simple style (`page`, `page_size`).

    Args:
        url: The full URL to parse.

    Returns:
        Dict containing pagination params if found.
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    pagination = {}
    if "page[number]" in params:
        pagination["page[number]"] = params["page[number]"][0]
    elif "page" in params:
        pagination["page"] = params["page"][0]

    if "page[size]" in params:
        pagination["page[size]"] = params["page[size]"][0]
    elif "page_size" in params:
        pagination["page_size"] = params["page_size"][0]

    return pagination


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove keys with None values from a dictionary.
    Useful for cleaning up query parameters and request payloads.
    """
    return {k: v for k, v in data.items() if v is not None}


def validate_endpoint_path(endpoint: str) -> str:
    """Validate and normalize API endpoint paths to reduce injection/smuggling risks."""
    if not isinstance(endpoint, str):
        raise EventyayValidationError("Endpoint path must be a string.", status_code=None)

    normalized = endpoint.strip()
    if not normalized:
        raise EventyayValidationError("Endpoint path cannot be empty.", status_code=None)

    if "://" in normalized or normalized.startswith("//"):
        raise EventyayValidationError(
            "Endpoint path must be relative and must not contain a URL scheme.",
            status_code=None,
        )

    if "\\" in normalized:
        raise EventyayValidationError(
            "Endpoint path must not contain backslashes.",
            status_code=None,
        )

    for char in normalized:
        codepoint = ord(char)
        if codepoint < 32 or codepoint == 127 or char in BIDI_CONTROL_CHARS:
            raise EventyayValidationError(
                "Endpoint path contains disallowed control characters.",
                status_code=None,
            )

    return normalized.lstrip("/")
