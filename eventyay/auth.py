from typing import Any, Dict, Optional

from ._transport import SyncTransportBase


class AuthMixin(SyncTransportBase):
    """Authentication and account-security related API operations."""

    def login(self, email: str, password: str, remember_me: bool = False) -> Dict[str, Any]:
        payload = {"email": email, "password": password, "remember_me": remember_me}
        return self._post("auth/login", json=payload)

    def logout(self, refresh_token: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if refresh_token is not None:
            payload["refresh_token"] = refresh_token
        return self._post("auth/logout", json=payload)

    def verify_password(self, password: str) -> Dict[str, Any]:
        return self._post("auth/verify-password", json={"password": password})

    def change_password(self, old_password: str, new_password: str) -> Dict[str, Any]:
        payload = {"old_password": old_password, "new_password": new_password}
        return self._post("auth/change-password", json=payload)

    def request_password_reset(self, email: str) -> Dict[str, Any]:
        return self._post("auth/reset-password", json={"email": email})

    def reset_password_with_token(self, token: str, new_password: str) -> Dict[str, Any]:
        payload = {"token": token, "password": new_password}
        return self._patch("auth/reset-password", json=payload)

    def resend_email_verification(self, email: str) -> Dict[str, Any]:
        return self._post("auth/resend-verification-email", json={"email": email})

    def verify_email(self, token: str) -> Dict[str, Any]:
        return self._post("auth/verify-email", json={"token": token})
