"""Stable error codes emitted by the Blaxel gateway proxy.

These codes appear in the ``X-Blaxel-Error-Code`` response header and the
``error.code`` field of the JSON body on gateway-synthesized error responses.

Usage::

    from blaxel.core.client.errors import GatewayError
    from blaxel.core.client.error_codes import WORKLOAD_UNAVAILABLE

    try:
        result = await some_api_call()
    except GatewayError as exc:
        if exc.error_code == WORKLOAD_UNAVAILABLE:
            # retry with backoff
            ...
"""

ROUTE_NOT_FOUND: str = "ROUTE_NOT_FOUND"
WORKLOAD_NOT_FOUND: str = "WORKLOAD_NOT_FOUND"
WORKSPACE_NOT_FOUND: str = "WORKSPACE_NOT_FOUND"
WORKLOAD_UNAVAILABLE: str = "WORKLOAD_UNAVAILABLE"
AUTHENTICATION_REQUIRED: str = "AUTHENTICATION_REQUIRED"
AUTHENTICATION_FAILED: str = "AUTHENTICATION_FAILED"
FORBIDDEN: str = "FORBIDDEN"
BAD_REQUEST: str = "BAD_REQUEST"
USAGE_LIMIT_EXCEEDED: str = "USAGE_LIMIT_EXCEEDED"
POLICY_VIOLATION: str = "POLICY_VIOLATION"

__all__ = [
    "ROUTE_NOT_FOUND",
    "WORKLOAD_NOT_FOUND",
    "WORKSPACE_NOT_FOUND",
    "WORKLOAD_UNAVAILABLE",
    "AUTHENTICATION_REQUIRED",
    "AUTHENTICATION_FAILED",
    "FORBIDDEN",
    "BAD_REQUEST",
    "USAGE_LIMIT_EXCEEDED",
    "POLICY_VIOLATION",
]
