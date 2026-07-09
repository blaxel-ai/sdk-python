"""Contains shared errors types that can be raised from API functions"""

from __future__ import annotations

import json
from typing import Any

import httpx


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


class GatewayError(Exception):
    """Raised when the Blaxel gateway proxy synthesizes an error response.

    The gateway sets ``X-Blaxel-Source: platform`` on every response it
    generates itself (as opposed to forwarding from the upstream workload).
    This exception exposes the stable error code and agent-readable metadata
    so callers can branch on ``error_code`` instead of parsing free-text
    messages.
    """

    def __init__(
        self,
        *,
        error_code: str,
        message: str,
        status_code: int,
        retryable: bool,
        action: str,
        do_not: str | None = None,
        docs_url: str | None = None,
        response: httpx.Response,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code
        self.retryable = retryable
        self.action = action
        self.do_not = do_not
        self.docs_url = docs_url
        self.response = response


def check_gateway_error(response: httpx.Response) -> None:
    """Raise :class:`GatewayError` if *response* is a gateway-synthesized error.

    Call this before any other response parsing so that gateway errors are
    surfaced consistently across generated and hand-written API calls.
    """
    if response.headers.get("X-Blaxel-Source") != "platform":
        return

    error_obj: dict[str, Any] = {}
    try:
        body = response.json()
        if isinstance(body, dict):
            error_obj = body.get("error", {})
            if not isinstance(error_obj, dict):
                error_obj = {}
    except (json.JSONDecodeError, ValueError):
        pass

    raise GatewayError(
        error_code=response.headers.get("X-Blaxel-Error-Code", ""),
        message=error_obj.get("message", response.text),
        status_code=response.status_code,
        retryable=bool(error_obj.get("retryable", False)),
        action=error_obj.get("action", ""),
        do_not=error_obj.get("do_not"),
        docs_url=error_obj.get("docs_url"),
        response=response,
    )


__all__ = ["UnexpectedStatus", "GatewayError", "check_gateway_error"]
