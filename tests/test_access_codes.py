"""Tests for Access Code related operations."""

from eventyay.models import AccessCode, AccessCodeList


class TestGetEventAccessCodes:
    def test_returns_access_code_list(self, mock_client, mock_response, sample_access_code):
        mock_client.session.get.return_value = mock_response({"data": [sample_access_code]})

        result = mock_client.get_event_access_codes("test-event")

        assert isinstance(result, AccessCodeList)
        assert len(result.data) == 1
        assert result.data[0].code == "VIPACCESS"


class TestGetAccessCode:
    def test_returns_access_code(self, mock_client, mock_response, sample_access_code):
        mock_client.session.get.return_value = mock_response(sample_access_code)

        result = mock_client.get_access_code("851")

        assert isinstance(result, AccessCode)
        assert result.id == 851
