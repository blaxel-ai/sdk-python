import asyncio
import random
import time
from collections.abc import Awaitable, Callable, Iterator
from typing import TypeVar

import httpx

from ..common.settings import settings

T = TypeVar("T")

TRANSIENT_RESET_MARKERS = (
    "ENHANCE_YOUR_CALM",
    "NGHTTP2_INTERNAL_ERROR",
    "ERR_HTTP2",
    "GOAWAY",
    "HTTP/2 session closed before response",
    "HTTP/2 session sent GOAWAY before response",
    "Connection reset by peer",
    "Server disconnected without sending a response",
)

TRANSIENT_ERROR_CODES = {
    "ECONNRESET",
    "ECONNREFUSED",
    "ETIMEDOUT",
    "EPIPE",
    "ERR_HTTP2_STREAM_ERROR",
    "ERR_HTTP2_GOAWAY_SESSION",
    "ERR_HTTP2_SESSION_ERROR",
}

DEFAULT_BASE_DELAY_SECONDS = 0.2
DEFAULT_MAX_DELAY_SECONDS = 2.0


def _walk_error_chain(error: BaseException) -> Iterator[BaseException]:
    current: BaseException | None = error
    seen: set[int] = set()
    for _ in range(5):
        if current is None or id(current) in seen:
            break
        seen.add(id(current))
        yield current
        current = current.__cause__ or current.__context__


def _has_http_response_status(error: BaseException) -> bool:
    for node in _walk_error_chain(error):
        response = getattr(node, "response", None)
        status = getattr(response, "status_code", None)
        if isinstance(status, int):
            return True
        status = getattr(node, "status_code", None)
        if isinstance(status, int):
            return True
    return False


def _collect_error_text(error: BaseException) -> tuple[list[str], list[str]]:
    messages: list[str] = []
    codes: list[str] = []
    for node in _walk_error_chain(error):
        messages.append(str(node))
        code = getattr(node, "code", None)
        if isinstance(code, str):
            codes.append(code)
        errno = getattr(node, "errno", None)
        if isinstance(errno, str):
            codes.append(errno)
    return messages, codes


def is_transient_reset_error(error: BaseException) -> bool:
    """True for transport-level drops that are safe to retry on idempotent calls."""
    if _has_http_response_status(error):
        return False
    if isinstance(error, httpx.TimeoutException | httpx.NetworkError | httpx.RemoteProtocolError):
        return True
    if not isinstance(error, httpx.TransportError):
        return False

    messages, codes = _collect_error_text(error)
    if any(code in TRANSIENT_ERROR_CODES for code in codes):
        return True
    return any(marker in message for message in messages for marker in TRANSIENT_RESET_MARKERS)


def _backoff_delay_seconds(
    attempt: int,
    base_delay_seconds: float,
    max_delay_seconds: float,
) -> float:
    if base_delay_seconds <= 0 or max_delay_seconds <= 0:
        return 0
    exponential = base_delay_seconds * (2 ** (attempt - 1))
    capped = min(exponential, max_delay_seconds)
    return capped + random.uniform(0, base_delay_seconds)


async def retry_on_transient_reset_async(
    fn: Callable[[], Awaitable[T]],
    *,
    retries: int | None = None,
    base_delay_seconds: float = DEFAULT_BASE_DELAY_SECONDS,
    max_delay_seconds: float = DEFAULT_MAX_DELAY_SECONDS,
) -> T:
    retry_budget = settings.sandbox_read_retries if retries is None else retries
    attempt = 0
    while True:
        try:
            return await fn()
        except Exception as error:
            attempt += 1
            if retry_budget <= 0 or attempt > retry_budget or not is_transient_reset_error(error):
                raise
            delay = _backoff_delay_seconds(attempt, base_delay_seconds, max_delay_seconds)
            if delay:
                await asyncio.sleep(delay)


def retry_on_transient_reset(
    fn: Callable[[], T],
    *,
    retries: int | None = None,
    base_delay_seconds: float = DEFAULT_BASE_DELAY_SECONDS,
    max_delay_seconds: float = DEFAULT_MAX_DELAY_SECONDS,
) -> T:
    retry_budget = settings.sandbox_read_retries if retries is None else retries
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as error:
            attempt += 1
            if retry_budget <= 0 or attempt > retry_budget or not is_transient_reset_error(error):
                raise
            delay = _backoff_delay_seconds(attempt, base_delay_seconds, max_delay_seconds)
            if delay:
                time.sleep(delay)
