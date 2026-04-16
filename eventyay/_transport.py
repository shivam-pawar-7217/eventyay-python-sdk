"""Transport contracts used by mixin classes for static typing."""

from typing import Any, Dict, Optional


class SyncTransportBase:
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError

    def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def _patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def _delete(self, endpoint: str) -> None:
        raise NotImplementedError


class AsyncTransportBase:
    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError

    async def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    async def _patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    async def _delete(self, endpoint: str) -> None:
        raise NotImplementedError
