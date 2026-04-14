"""Tests for Role-related operations."""

from eventyay.models import Role, RoleList


class TestGetEventRoles:
    def test_returns_role_list(self, mock_client, mock_response, sample_role):
        mock_client.session.get.return_value = mock_response({"data": [sample_role]})

        result = mock_client.get_event_roles("test-event")

        assert isinstance(result, RoleList)
        assert len(result.data) == 1
        assert result.data[0].name == "organizer"


class TestGetRole:
    def test_returns_role(self, mock_client, mock_response, sample_role):
        mock_client.session.get.return_value = mock_response({"data": sample_role})

        result = mock_client.get_role("test-event", "1201")

        assert isinstance(result, Role)
        assert result.title_name == "Event Organizer"
