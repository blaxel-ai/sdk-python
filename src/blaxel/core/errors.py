"""Unified error hierarchy for Blaxel SDK.

All domain-specific API errors (ControlPlaneError, SandboxAPIError,
DriveAPIError, VolumeAPIError) inherit from BlaxelAPIError, giving
callers a single base class they can catch.
"""

import httpx


class BlaxelAPIError(Exception):
    """Base exception for all Blaxel API errors.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code of the error response, if available.
        error_code: Machine-readable error code, if available.
        response: The raw ``httpx.Response`` that triggered the error,
            if available.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        error_code: str | None = None,
        response: httpx.Response | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.response = response
