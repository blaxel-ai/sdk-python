"""Contains shared error types that can be raised from API functions."""

import json
import re
from datetime import timezone
from email.utils import format_datetime, parsedate_to_datetime
from http import HTTPStatus
from typing import Any, Mapping

_MAX_JSON_INSPECTION_BYTES = 64 * 1024
_STABLE_CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{1,127}$")


def _json_body(content: bytes) -> dict[str, Any] | None:
    if not content or len(content) > _MAX_JSON_INSPECTION_BYTES:
        return None
    try:
        value = json.loads(content)
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


def _safe_body_preview(content: bytes) -> str:
    if not content:
        return "<empty body>"
    return f"<response body: {len(content)} bytes>"


def _safe_retry_after_value(value: Any) -> str | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and 0 <= value <= 9_999_999_999:
        return str(value)
    if not isinstance(value, str):
        return None

    value = value.strip()
    if re.fullmatch(r"[0-9]{1,10}", value):
        return value
    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if retry_at is None or retry_at.tzinfo is None:
        return None
    return format_datetime(retry_at.astimezone(timezone.utc), usegmt=True)


def _extract_error_metadata(
    content: bytes,
) -> tuple[str | None, bool | None, str | None]:
    parsed = _json_body(content)
    if parsed is None:
        return None, None, None

    nested_error = parsed.get("error")
    sources = [nested_error, parsed] if isinstance(nested_error, dict) else [parsed]

    error_code: str | None = None
    retryable: bool | None = None
    retry_after: str | None = None
    for source in sources:
        if not isinstance(source, dict):
            continue
        if error_code is None:
            for key in ("code", "error_code", "type"):
                candidate = source.get(key)
                if isinstance(candidate, str) and _STABLE_CODE_PATTERN.fullmatch(candidate):
                    error_code = candidate
                    break
        candidate_retryable = source.get("retryable")
        if retryable is None and isinstance(candidate_retryable, bool):
            retryable = candidate_retryable
        if retry_after is None:
            for key in ("retry_after", "retryAfter", "retry_after_seconds"):
                retry_after = _safe_retry_after_value(source.get(key))
                if retry_after is not None:
                    break

    return error_code, retryable, retry_after


def _retry_after_header(headers: Mapping[str, str] | None) -> str | None:
    if headers is None:
        return None
    for key, value in headers.items():
        if isinstance(key, str) and key.lower() == "retry-after":
            return _safe_retry_after_value(value)
    return None


class UnexpectedStatus(Exception):
    """Raised when an API returns a status absent from its OpenAPI contract."""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content
        self.body_preview = _safe_body_preview(content)

        super().__init__(f"Unexpected HTTP status {status_code}")


class APIStatusError(UnexpectedStatus):
    """Base class for typed HTTP status errors not modeled by an endpoint."""

    def __init__(
        self,
        status_code: int,
        content: bytes,
        headers: Mapping[str, str] | None = None,
    ):
        self.error_code, self.retryable, body_retry_after = _extract_error_metadata(content)
        self.retry_after = _retry_after_header(headers) or body_retry_after
        self.retry_after_seconds = (
            int(self.retry_after)
            if self.retry_after is not None and self.retry_after.isdigit()
            else None
        )
        if self.retryable is None and self.retry_after is not None:
            self.retryable = True

        super().__init__(status_code, content)

        try:
            status_name = HTTPStatus(status_code).phrase
        except ValueError:
            status_name = "HTTP error"
        Exception.__init__(self, f"HTTP {status_code} {status_name}")


class ConflictError(APIStatusError):
    """Raised for an undocumented HTTP 409 conflict response."""


class RateLimitError(APIStatusError):
    """Raised for an undocumented HTTP 429 rate-limit response."""


def from_response(
    status_code: int,
    content: bytes,
    headers: Mapping[str, str] | None = None,
) -> UnexpectedStatus:
    """Build the most specific safe error for an undocumented response."""
    if status_code == HTTPStatus.CONFLICT:
        return ConflictError(status_code, content, headers)
    if status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return RateLimitError(status_code, content, headers)
    return APIStatusError(status_code, content, headers)


__all__ = [
    "APIStatusError",
    "ConflictError",
    "RateLimitError",
    "UnexpectedStatus",
    "from_response",
]
