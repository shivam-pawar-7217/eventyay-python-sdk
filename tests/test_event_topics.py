"""Tests for Event Topic related operations."""

from eventyay.models import EventTopic, EventTopicList


class TestGetEventTopics:
    def test_returns_event_topic_list(self, mock_client, mock_response, sample_event_topic):
        mock_client.session.get.return_value = mock_response({"data": [sample_event_topic]})

        result = mock_client.get_event_topics()

        assert isinstance(result, EventTopicList)
        assert len(result.data) == 1
        assert result.data[0].name == "technology"


class TestGetEventTopic:
    def test_returns_event_topic(self, mock_client, mock_response, sample_event_topic):
        mock_client.session.get.return_value = mock_response(sample_event_topic)

        result = mock_client.get_event_topic("1602")

        assert isinstance(result, EventTopic)
        assert result.id == 1602
