"""Tests for Sponsor-related operations."""

from eventyay.models import Sponsor, SponsorList


class TestGetEventSponsors:
    def test_returns_sponsor_list(self, mock_client, mock_response, sample_sponsor):
        mock_client.session.get.return_value = mock_response({"data": [sample_sponsor]})

        result = mock_client.get_event_sponsors("test-event")

        assert isinstance(result, SponsorList)
        assert len(result.data) == 1
        assert result.data[0].name == "TechCorp"
        assert result.data[0].level == "Gold"


class TestGetSponsor:
    def test_returns_sponsor(self, mock_client, mock_response, sample_sponsor):
        mock_client.session.get.return_value = mock_response(sample_sponsor)

        result = mock_client.get_sponsor("test-event", "701")

        assert isinstance(result, Sponsor)
        assert result.url == "https://techcorp.example.com"
