"""Tests for Service related operations."""

from eventyay.models import Service, ServiceList


class TestGetServices:
    def test_returns_service_list(self, mock_client, mock_response, sample_service):
        mock_client.session.get.return_value = mock_response({"data": [sample_service]})

        result = mock_client.get_services()

        assert isinstance(result, ServiceList)
        assert len(result.data) == 1
        assert result.data[0].name == "stripe"


class TestGetService:
    def test_returns_service(self, mock_client, mock_response, sample_service):
        mock_client.session.get.return_value = mock_response(sample_service)

        result = mock_client.get_service("1703")

        assert isinstance(result, Service)
        assert result.id == 1703
