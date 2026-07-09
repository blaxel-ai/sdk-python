"""Contains shared errors types that can be raised from API functions"""

from __future__ import annotations


class BlaxelAPIError(Exception):
    """Base exception for all Blaxel API errors.

    Allows users to catch all Blaxel API errors with a single except clause::

        from blaxel.core import BlaxelAPIError
        try:
            ...
        except BlaxelAPIError as e:
            print(e.status_code, e.error_code)
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        error_code: str | None = None,
        response: object | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.response = response


class UnexpectedStatus(BlaxelAPIError):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.content = content
        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}",
            status_code=status_code,
        )


def error_to_exception(error: object) -> BlaxelAPIError:
    """Convert an ``Error`` data-model instance to a ``BlaxelAPIError``.

    This is a free function rather than a method on ``Error`` because that class
    is auto-generated and must not be edited directly.
    """
    from .models.error import Error
    from .types import UNSET

    if not isinstance(error, Error):
        raise TypeError(f"Expected Error instance, got {type(error)}")

    status_code = error.code if error.code is not UNSET else None
    message = error.message if error.message is not UNSET else error.error

    return BlaxelAPIError(
        message=str(message),
        status_code=status_code,
        error_code=error.error,
    )


__all__ = ["BlaxelAPIError", "UnexpectedStatus", "error_to_exception"]
