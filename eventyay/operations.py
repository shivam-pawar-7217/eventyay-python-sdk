from typing import Any, Dict

from ._transport import SyncTransportBase


class OperationsMixin(SyncTransportBase):
    """Operational endpoints for copy/upload-image workflows."""

    def copy_event(self, event_id: str) -> Dict[str, Any]:
        return self._post(f"events/{event_id}/copy")

    def upload_image(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("upload/image", json=payload)
