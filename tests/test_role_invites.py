"""Tests for Role Invite related operations."""

from unittest.mock import Mock

from eventyay.models import RoleInvite, RoleInviteList


class TestGetRoleInvites:
    def test_returns_role_invite_list(self, mock_client, mock_response, sample_role_invite):
        mock_client.session.get.return_value = mock_response({"data": [sample_role_invite]})

        result = mock_client.get_role_invites()

        assert isinstance(result, RoleInviteList)
        assert len(result.data) == 1
        assert result.data[0].email == "organizer@example.com"


class TestGetRoleInvite:
    def test_returns_role_invite(self, mock_client, mock_response, sample_role_invite):
        mock_client.session.get.return_value = mock_response(sample_role_invite)

        result = mock_client.get_role_invite("1251")

        assert isinstance(result, RoleInvite)
        assert result.status == "pending"


class TestDeleteRoleInvite:
    def test_deletes_role_invite(self, mock_client):
        response = Mock()
        response.status_code = 204
        mock_client.session.delete.return_value = response

        result = mock_client.delete_role_invite("1251")

        assert result is True
