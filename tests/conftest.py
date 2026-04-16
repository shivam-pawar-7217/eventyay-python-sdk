"""
Shared test fixtures for the Eventyay SDK test suite.

Provides mock clients and sample data for consistent test setup.
"""

from unittest.mock import Mock

import pytest

from eventyay.client import EventyayClient


@pytest.fixture
def mock_client():
    """Creates an EventyayClient with a mocked requests session."""
    client = EventyayClient(api_key="test-key-1234")
    client.session = Mock()
    return client


@pytest.fixture
def mock_response():
    """Creates a factory for mock HTTP responses."""

    def _make_response(json_data, status_code=200):
        response = Mock()
        response.json.return_value = json_data
        response.status_code = status_code
        response.text = str(json_data)
        response.raise_for_status = Mock()
        if status_code >= 400:
            from requests.exceptions import HTTPError

            response.raise_for_status.side_effect = HTTPError(response=response)
        return response

    return _make_response


# ── Sample Data ──────────────────────────────────────────────


@pytest.fixture
def sample_organizer():
    return {
        "id": 1,
        "name": "FOSSASIA",
        "description": "Open source org",
        "url": "https://fossasia.org",
    }


@pytest.fixture
def sample_event():
    return {
        "id": 1,
        "name": "Test Conference",
        "identifier": "test-conf-2026",
        "starts_at": "2026-06-01T09:00:00Z",
        "ends_at": "2026-06-03T18:00:00Z",
        "timezone": "UTC",
        "privacy": "public",
        "location_name": "Berlin",
        "online": False,
    }


@pytest.fixture
def sample_event_type():
    return {"id": 1601, "name": "conference"}


@pytest.fixture
def sample_event_topic():
    return {"id": 1602, "name": "technology"}


@pytest.fixture
def sample_event_sub_topic():
    return {"id": 1603, "name": "python"}


@pytest.fixture
def sample_notification():
    return {
        "id": 1701,
        "title": "Welcome",
        "message": "Welcome to Eventyay",
        "is_read": False,
    }


@pytest.fixture
def sample_page():
    return {
        "id": 1702,
        "name": "about",
        "title": "About Eventyay",
        "description": "About page",
    }


@pytest.fixture
def sample_service():
    return {
        "id": 1703,
        "name": "stripe",
        "enabled": True,
    }


@pytest.fixture
def sample_generic_resource():
    return {
        "id": 1901,
        "name": "generic-resource",
    }


@pytest.fixture
def sample_attendee():
    return {
        "id": 101,
        "email": "alice@test.com",
        "firstname": "Alice",
        "lastname": "Smith",
        "isCheckedIn": True,
    }


@pytest.fixture
def sample_speaker():
    return {
        "id": 201,
        "name": "Dr. Jane Doe",
        "email": "jane@speaker.com",
        "short_biography": "AI researcher",
    }


@pytest.fixture
def sample_session():
    return {
        "id": 301,
        "title": "Keynote: Future of Open Source",
        "starts_at": "2026-06-01T09:30:00Z",
    }


@pytest.fixture
def sample_ticket():
    return {"id": 401, "name": "General Admission", "type": "paid", "price": 25.0, "quantity": 500}


@pytest.fixture
def sample_track():
    return {
        "id": 501,
        "name": "AI & ML",
        "color": "#3498db",
        "description": "Artificial Intelligence track",
    }


@pytest.fixture
def sample_microlocation():
    return {"id": 601, "name": "Main Hall", "floor": 1, "room": "A101"}


@pytest.fixture
def sample_sponsor():
    return {"id": 701, "name": "TechCorp", "level": "Gold", "url": "https://techcorp.example.com"}


@pytest.fixture
def sample_discount_code():
    return {"id": 801, "code": "EARLYBIRD", "type": "percent", "value": 20.0, "is_active": True}


@pytest.fixture
def sample_access_code():
    return {
        "id": 851,
        "code": "VIPACCESS",
        "is_active": True,
        "tickets_number": 100,
    }


@pytest.fixture
def sample_order():
    return {
        "id": 901,
        "identifier": "ORD-001",
        "status": "completed",
        "amount": 50.0,
        "paid_via": "stripe",
    }


@pytest.fixture
def sample_tax():
    return {
        "id": 1001,
        "name": "GST",
        "rate": 18.0,
        "is_tax_included_in_price": False,
        "country": "IN",
    }


@pytest.fixture
def sample_user():
    return {"id": 1101, "email": "admin@eventyay.com", "first_name": "Admin", "last_name": "User"}


@pytest.fixture
def sample_role():
    return {"id": 1201, "name": "organizer", "title_name": "Event Organizer"}


@pytest.fixture
def sample_role_invite():
    return {
        "id": 1251,
        "email": "organizer@example.com",
        "token": "invite-token-123",
        "status": "pending",
    }


@pytest.fixture
def sample_ticket_tag():
    return {
        "id": 1451,
        "name": "VIP",
        "color": "#ff8800",
        "is_active": True,
    }


@pytest.fixture
def sample_feedback():
    return {"id": 1301, "rating": 4.5, "comment": "Great event!", "session_id": 301}


@pytest.fixture
def sample_setting():
    return {
        "id": 1401,
        "app_name": "Eventyay",
        "app_environment": "production",
        "frontend_url": "https://eventyay.com",
    }
