"""Tests for User-related operations."""

from eventyay.models import User, UserList


class TestGetUsers:
    def test_returns_user_list(self, mock_client, mock_response, sample_user):
        mock_client.session.get.return_value = mock_response({"data": [sample_user]})

        result = mock_client.get_users()

        assert isinstance(result, UserList)
        assert len(result.data) == 1
        assert result.data[0].email == "admin@eventyay.com"


class TestGetUser:
    def test_returns_user(self, mock_client, mock_response, sample_user):
        mock_client.session.get.return_value = mock_response({"data": sample_user})

        result = mock_client.get_user("1101")

        assert isinstance(result, User)
        assert result.first_name == "Admin"

    def test_get_self(self, mock_client, mock_response, sample_user):
        mock_client.session.get.return_value = mock_response({"data": sample_user})

        mock_client.get_user("me")

        args, _ = mock_client.session.get.call_args
        assert args[0].endswith("users/me")


class TestUpdateUser:
    def test_updates_user(self, mock_client, mock_response, sample_user):
        updated = {**sample_user, "first_name": "Updated"}
        mock_client.session.patch.return_value = mock_response({"data": updated})

        result = mock_client.update_user("1101", {"first_name": "Updated"})

        assert result.first_name == "Updated"


class TestGetAllUsers:
    def test_fetches_all_pages(self, mock_client, mock_response, sample_user):
        page1 = mock_response({"data": [sample_user], "links": {"next": "http://api/users?page=2"}})
        page2 = mock_response(
            {
                "data": [{**sample_user, "id": 1102, "email": "user2@test.com"}],
                "links": {"next": None},
            }
        )
        mock_client.session.get.side_effect = [page1, page2]

        result = mock_client.get_all_users()

        assert len(result) == 2
