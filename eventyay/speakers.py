from typing import Optional
from .models import Speaker


class SpeakersMixin:
    """
    Mixin class providing methods for interacting with standalone Speaker endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_speaker(self, event_identifier: str, speaker_id: str) -> Speaker:
        """
        Fetches details for a single specific speaker.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            speaker_id (str): The unique identifier of the speaker.

        Returns:
            Speaker: The detailed Speaker object.
        """
        response_data = self._get(f"events/{event_identifier}/speakers/{speaker_id}")
        return Speaker(**response_data)
