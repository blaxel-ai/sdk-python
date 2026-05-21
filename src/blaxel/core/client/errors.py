"""Contains shared errors types that can be raised from API functions"""

import httpx

from ..errors import BlaxelAPIError
from .models.error import Error
from .types import UNSET


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


class ControlPlaneError(BlaxelAPIError):
    """Raised when a control-plane API endpoint returns an error response (4xx/5xx).

    The original ``Error`` data model is preserved on ``error_model`` so
    callers can inspect structured fields if needed.
    """

    def __init__(self, error: Error, response: httpx.Response):
        message = error.message if not isinstance(error.message, type(UNSET)) else error.error
        status_code = (
            error.code if not isinstance(error.code, type(UNSET)) else response.status_code
        )
        super().__init__(
            message=str(message),
            status_code=int(status_code) if status_code is not None else response.status_code,
            error_code=error.error,
            response=response,
        )
        self.error_model = error


__all__ = ["UnexpectedStatus", "ControlPlaneError"]
