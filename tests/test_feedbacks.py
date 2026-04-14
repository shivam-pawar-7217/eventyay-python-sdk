"""Tests for Feedback-related operations."""

from eventyay.models import Feedback, FeedbackList


class TestGetEventFeedbacks:
    def test_returns_feedback_list(self, mock_client, mock_response, sample_feedback):
        mock_client.session.get.return_value = mock_response({"data": [sample_feedback]})

        result = mock_client.get_event_feedbacks("test-event")

        assert isinstance(result, FeedbackList)
        assert len(result.data) == 1
        assert result.data[0].rating == 4.5
        assert result.data[0].comment == "Great event!"


class TestGetFeedback:
    def test_returns_feedback(self, mock_client, mock_response, sample_feedback):
        mock_client.session.get.return_value = mock_response({"data": sample_feedback})

        result = mock_client.get_feedback("test-event", "1301")

        assert isinstance(result, Feedback)
        assert result.session_id == 301
