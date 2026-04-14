"""
Eventyay SDK Utilities

Helper functions for API response parsing, pagination, and data transformation.
Includes JSON:API specification support for dasherized field name conversion.
"""

from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse


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


def parse_jsonapi_resource(response_data: Dict[str, Any]) -> Dict[str, Any]:
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
    # If response has 'data' key with 'attributes', it's JSON:API format
    if "data" in response_data and isinstance(response_data["data"], dict):
        data = response_data["data"]

        # JSON:API resource object has 'type', 'id', 'attributes'
        if "attributes" in data:
            result = _convert_keys(data["attributes"])
            # Include the id from the resource object
            if "id" in data:
                try:
                    result["id"] = int(data["id"])
                except (ValueError, TypeError):
                    result["id"] = data["id"]
            return result
        else:
            # It's a {"data": {...}} wrapper without attributes (our old format)
            return _convert_keys(data)

    # Plain dict response (no 'data' wrapper) — backward compatible
    return _convert_keys(response_data)


def parse_jsonapi_list(response_data: Dict[str, Any]) -> Dict[str, Any]:
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
    if "data" not in response_data:
        return response_data

    data = response_data["data"]

    # If data is a list, parse each item
    if isinstance(data, list):
        parsed_items = []
        for item in data:
            if isinstance(item, dict) and "attributes" in item:
                # JSON:API resource object
                flat = _convert_keys(item["attributes"])
                if "id" in item:
                    try:
                        flat["id"] = int(item["id"])
                    except (ValueError, TypeError):
                        flat["id"] = item["id"]
                parsed_items.append(flat)
            else:
                # Already a flat dict
                parsed_items.append(_convert_keys(item) if isinstance(item, dict) else item)

        result = {"data": parsed_items}

        # Preserve pagination links and meta
        if "links" in response_data:
            result["links"] = response_data["links"]
        if "meta" in response_data:
            result["meta"] = response_data["meta"]

        return result

    # data is a single resource (not a list) — shouldn't happen for list endpoints
    # but handle gracefully
    return response_data


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

    result = {}
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
