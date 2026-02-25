from .models import Feedback, FeedbackList


class FeedbacksMixin:
    """
    Mixin for Feedback-related API endpoints.
    Requires self._get() to be provided by the central client.
    """

    def get_event_feedbacks(
        self, event_id: str, page: int = 1, page_size: int = 25
    ) -> FeedbackList:
        """
        Retrieves a paginated list of feedbacks for an event.

        Args:
            event_id (str): The event identifier.
            page (int): The page number to fetch.
            page_size (int): Number of results per page.

        Returns:
            FeedbackList: Paginated feedback entries.
        """
        params = {"page[number]": page, "page[size]": page_size}
        response = self._get(
            f"events/{event_id}/feedbacks", params=params
        )
        return FeedbackList(**response)

    def get_feedback(
        self, event_id: str, feedback_id: str
    ) -> Feedback:
        """
        Retrieves a single feedback entry.

        Args:
            event_id (str): The event identifier.
            feedback_id (str): The ID of the feedback.

        Returns:
            Feedback: A parsed Pydantic `Feedback` object.
        """
        response = self._get(
            f"events/{event_id}/feedbacks/{feedback_id}"
        )
        return Feedback(**response["data"])
