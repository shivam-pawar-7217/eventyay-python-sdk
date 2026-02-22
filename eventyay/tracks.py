from typing import Optional
from .models import Track, TrackList


class TracksMixin:
    """
    Mixin class providing methods for interacting with Track-related endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_event_tracks(self, event_identifier: str,
                         page: int = 1,
                         page_size: int = 10) -> TrackList:
        """
        Retrieves a paginated list of tracks for a specific event.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): Number of tracks per page. Defaults to 10.

        Returns:
            TrackList: A Pydantic model containing the list of tracks
                       and pagination metadata.
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        response_data = self._get(
            f'events/{event_identifier}/tracks', params=params
        )
        return TrackList(**response_data)

    def get_track(self, event_identifier: str, track_id: str) -> Track:
        """
        Fetches details for a single specific track.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            track_id (str): The unique identifier of the track.

        Returns:
            Track: The detailed Track object.
        """
        response_data = self._get(
            f'events/{event_identifier}/tracks/{track_id}'
        )
        return Track(**response_data)
