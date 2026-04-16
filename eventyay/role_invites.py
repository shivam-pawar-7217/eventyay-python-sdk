from typing import Optional

from ._transport import SyncTransportBase
from .models import RoleInvite, RoleInviteList
from .utils import build_jsonapi_payload, parse_jsonapi_list, parse_jsonapi_resource


class RoleInvitesMixin(SyncTransportBase):
    """Mixin class for interacting with Role Invite endpoints."""

    def get_role_invites(self, page: int = 1, page_size: int = 25) -> RoleInviteList:
        """Retrieve paginated role invites."""
        params = {"page[number]": page, "page[size]": page_size}
        response_data = self._get("role-invites", params=params)
        return RoleInviteList(
            **parse_jsonapi_list(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def get_role_invite(self, invite_id: str) -> RoleInvite:
        """Fetch a single role invite by ID."""
        response_data = self._get(f"role-invites/{invite_id}")
        return RoleInvite(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def create_role_invite(
        self,
        email: str,
        role_id: str,
        event_id: str,
        idempotency_key: Optional[str] = None,
    ) -> RoleInvite:
        """Create a role invite for a user on an event."""
        payload = build_jsonapi_payload(
            "role-invite",
            {"email": email, "role_id": role_id, "event_id": event_id},
        )
        response_data = self._post("role-invites", json=payload, idempotency_key=idempotency_key)
        return RoleInvite(
            **parse_jsonapi_resource(response_data, strict=getattr(self, "strict_jsonapi", False))
        )

    def delete_role_invite(self, invite_id: str) -> bool:
        """Delete a role invite by ID."""
        self._delete(f"role-invites/{invite_id}")
        return True
