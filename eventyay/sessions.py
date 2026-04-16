from ._transport import SyncTransportBase
from .models import Session
from .utils import parse_jsonapi_resource


class SessionsMixin(SyncTransportBase):
    """
    Mixin class providing methods for interacting with standalone Session endpoints.

    This mixin is intended to be used with the main EventyayClient class.
    """

    def get_session(self, event_identifier: str, session_id: str) -> Session:
        """
        Fetches details for a single specific session.

        Args:
            event_identifier (str): The unique identifier or slug of the event.
            session_id (str): The unique identifier of the session.

        Returns:
            Session: The detailed Session object.
        """
        response_data = self._get(f"events/{event_identifier}/sessions/{session_id}")
        return Session(**parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False)))
