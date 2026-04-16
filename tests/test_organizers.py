"""Tests for Organizer-related operations."""

from unittest.mock import Mock

from eventyay.models import Organizer, OrganizerList


class TestGetOrganizers:
    def test_returns_organizer_list(self, mock_client, mock_response, sample_organizer):
        mock_client.session.get.return_value = mock_response({"data": [sample_organizer]})

        result = mock_client.get_organizers()

        assert isinstance(result, OrganizerList)
        assert len(result.data) == 1
        assert result.data[0].name == "FOSSASIA"

    def test_pagination_params(self, mock_client, mock_response, sample_organizer):
        mock_client.session.get.return_value = mock_response({"data": [sample_organizer]})

        mock_client.get_organizers(page=3, page_size=25)

        _, kwargs = mock_client.session.get.call_args
        assert kwargs["params"]["page[number]"] == 3
        assert kwargs["params"]["page[size]"] == 25

    def test_calls_non_trailing_slash_endpoint(self, mock_client, mock_response, sample_organizer):
        mock_client.session.get.return_value = mock_response({"data": [sample_organizer]})

        mock_client.get_organizers()

        args, _ = mock_client.session.get.call_args
        assert args[0].endswith("/organizers")


class TestGetOrganizer:
    def test_returns_organizer(self, mock_client, mock_response, sample_organizer):
        mock_client.session.get.return_value = mock_response(sample_organizer)

        result = mock_client.get_organizer("fossasia")

        assert isinstance(result, Organizer)
        assert result.id == 1
        assert result.name == "FOSSASIA"

    def test_correct_endpoint(self, mock_client, mock_response, sample_organizer):
        mock_client.session.get.return_value = mock_response(sample_organizer)

        mock_client.get_organizer("my-org")

        args, _ = mock_client.session.get.call_args
        assert args[0].endswith("organizers/my-org")


class TestGetAllOrganizers:
    def test_fetches_all_pages(self, mock_client, mock_response, sample_organizer):
        page1 = mock_response(
            {"data": [sample_organizer], "links": {"next": "http://api/organizers?page=2"}}
        )
        page2 = mock_response(
            {"data": [{**sample_organizer, "id": 2, "name": "Mozilla"}], "links": {"next": None}}
        )
        mock_client.session.get.side_effect = [page1, page2]

        result = mock_client.get_all_organizers()

        assert len(result) == 2


class TestCreateOrganizer:
    def test_creates_organizer(self, mock_client, mock_response, sample_organizer):
        mock_client.session.post.return_value = mock_response(sample_organizer)

        result = mock_client.create_organizer(name="FOSSASIA", description="Open source org")

        assert isinstance(result, Organizer)
        assert result.name == "FOSSASIA"


class TestUpdateOrganizer:
    def test_updates_organizer(self, mock_client, mock_response, sample_organizer):
        updated = {**sample_organizer, "name": "Updated Org"}
        mock_client.session.patch.return_value = mock_response(updated)

        result = mock_client.update_organizer("fossasia", name="Updated Org")

        assert result.name == "Updated Org"


class TestDeleteOrganizer:
    def test_deletes_organizer(self, mock_client):
        response = Mock()
        response.status_code = 204
        mock_client.session.delete.return_value = response

        result = mock_client.delete_organizer("fossasia")

        assert result is True
