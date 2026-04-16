"""Tests for Event Sub Topic related operations."""

from eventyay.models import EventSubTopic, EventSubTopicList


class TestGetEventSubTopics:
    def test_returns_event_sub_topic_list(self, mock_client, mock_response, sample_event_sub_topic):
        mock_client.session.get.return_value = mock_response({"data": [sample_event_sub_topic]})

        result = mock_client.get_event_sub_topics()

        assert isinstance(result, EventSubTopicList)
        assert len(result.data) == 1
        assert result.data[0].name == "python"


class TestGetEventSubTopic:
    def test_returns_event_sub_topic(self, mock_client, mock_response, sample_event_sub_topic):
        mock_client.session.get.return_value = mock_response(sample_event_sub_topic)

        result = mock_client.get_event_sub_topic("1603")

        assert isinstance(result, EventSubTopic)
        assert result.id == 1603
