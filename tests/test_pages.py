"""Tests for Page related operations."""

from eventyay.models import Page, PageList


class TestGetPages:
    def test_returns_page_list(self, mock_client, mock_response, sample_page):
        mock_client.session.get.return_value = mock_response({"data": [sample_page]})

        result = mock_client.get_pages()

        assert isinstance(result, PageList)
        assert len(result.data) == 1
        assert result.data[0].name == "about"


class TestGetPage:
    def test_returns_page(self, mock_client, mock_response, sample_page):
        mock_client.session.get.return_value = mock_response(sample_page)

        result = mock_client.get_page("1702")

        assert isinstance(result, Page)
        assert result.id == 1702
