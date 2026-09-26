"""Transient-5xx retry behavior for the generated control-plane HTTP client.

Regression coverage for SDK-PYTHON-11K: a momentary ``502 Bad Gateway`` from the
API proxy used to surface as an ``UnexpectedStatus`` on idempotent calls such as
``get_drive``. The client now replays idempotent requests a bounded number of
times on transient gateway failures (502/503/504).
"""

import sys

import httpx
import pytest

from blaxel.core.client import errors
from blaxel.core.client.api.drives import create_drive, get_drive
from blaxel.core.client.client import (
    Client,
    _AsyncRetryTransport,
    _client_max_retries,
    _RetryTransport,
    _should_retry_transient,
)
from blaxel.core.client.models.drive import Drive

# The `blaxel.core.client` package re-exports the `client` singleton, which
# shadows the `client` submodule for `import ... as`; reach the module object
# through sys.modules so we can patch its backoff helper.
client_module = sys.modules["blaxel.core.client.client"]


@pytest.fixture(autouse=True)
def no_retry_sleep(monkeypatch):
    monkeypatch.setattr(client_module, "_retry_backoff_seconds", lambda *_: 0)


def _drive_body() -> bytes:
    return b'{"metadata": {"name": "test-drive"}, "spec": {}}'


class _CountingSyncTransport(httpx.BaseTransport):
    """Wrapped transport that plays back a fixed status sequence and counts calls."""

    def __init__(self, statuses: list[int], *, body: bytes = _drive_body()):
        self._statuses = statuses
        self._body = body
        self.methods: list[str] = []

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        index = min(len(self.methods), len(self._statuses) - 1)
        self.methods.append(request.method)
        status = self._statuses[index]
        content = self._body if status == 200 else b"<html>502 Bad Gateway</html>"
        return httpx.Response(status, content=content, request=request)


class _CountingAsyncTransport(httpx.AsyncBaseTransport):
    def __init__(self, statuses: list[int], *, body: bytes = _drive_body()):
        self._statuses = statuses
        self._body = body
        self.methods: list[str] = []

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        index = min(len(self.methods), len(self._statuses) - 1)
        self.methods.append(request.method)
        status = self._statuses[index]
        content = self._body if status == 200 else b"<html>502 Bad Gateway</html>"
        return httpx.Response(status, content=content, request=request)


def _client_with_sync_transport(inner: httpx.BaseTransport, retries: int) -> Client:
    return Client(
        base_url="https://api.blaxel.test",
        httpx_args={"transport": _RetryTransport(inner, retries)},
    )


def _client_with_async_transport(inner: httpx.AsyncBaseTransport, retries: int) -> Client:
    return Client(
        base_url="https://api.blaxel.test",
        httpx_args={"transport": _AsyncRetryTransport(inner, retries)},
    )


def test_retry_predicate_only_covers_idempotent_transient_5xx():
    get_502 = httpx.Request("GET", "https://api.blaxel.test/drives/x")
    post_502 = httpx.Request("POST", "https://api.blaxel.test/drives")

    assert _should_retry_transient(get_502, 502)
    assert _should_retry_transient(get_502, 503)
    assert _should_retry_transient(get_502, 504)
    assert not _should_retry_transient(get_502, 500)
    assert not _should_retry_transient(get_502, 200)
    assert not _should_retry_transient(post_502, 502)


def test_retry_budget_env_override(monkeypatch):
    monkeypatch.delenv("BL_CLIENT_RETRIES", raising=False)
    assert _client_max_retries() == 2

    monkeypatch.setenv("BL_CLIENT_RETRIES", "5")
    assert _client_max_retries() == 5

    monkeypatch.setenv("BL_CLIENT_RETRIES", "0")
    assert _client_max_retries() == 0

    monkeypatch.setenv("BL_CLIENT_RETRIES", "not-a-number")
    assert _client_max_retries() == 2

    monkeypatch.setenv("BL_CLIENT_RETRIES", "-3")
    assert _client_max_retries() == 2


def test_default_client_wraps_transport_with_retry():
    client = Client(base_url="https://api.blaxel.test")
    assert isinstance(client.get_httpx_client()._transport, _RetryTransport)


def test_custom_transport_is_respected_without_wrapping():
    inner = httpx.MockTransport(
        lambda request: httpx.Response(200, content=_drive_body(), request=request)
    )
    client = Client(base_url="https://api.blaxel.test", httpx_args={"transport": inner})
    assert client.get_httpx_client()._transport is inner


def test_get_drive_retries_then_succeeds_on_transient_502():
    inner = _CountingSyncTransport([502, 200])
    client = _client_with_sync_transport(inner, retries=2)

    result = get_drive.sync(drive_name="test-drive", client=client)

    assert isinstance(result, Drive)
    assert inner.methods == ["GET", "GET"]


def test_get_drive_gives_up_after_budget_and_raises():
    inner = _CountingSyncTransport([502])
    client = _client_with_sync_transport(inner, retries=2)

    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        get_drive.sync(drive_name="test-drive", client=client)

    assert exc_info.value.status_code == 502
    # initial attempt + 2 retries
    assert inner.methods == ["GET", "GET", "GET"]


def test_create_drive_post_is_not_retried_on_502():
    inner = _CountingSyncTransport([502, 200])
    client = _client_with_sync_transport(inner, retries=2)

    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        create_drive.sync(client=client, body=Drive(metadata={"name": "d"}, spec={}))  # type: ignore[arg-type]

    assert exc_info.value.status_code == 502
    assert inner.methods == ["POST"]


@pytest.mark.asyncio
async def test_async_get_drive_retries_then_succeeds_on_transient_502():
    inner = _CountingAsyncTransport([503, 502, 200])
    client = _client_with_async_transport(inner, retries=2)

    result = await get_drive.asyncio(drive_name="test-drive", client=client)

    assert isinstance(result, Drive)
    assert inner.methods == ["GET", "GET", "GET"]
    await client.get_async_httpx_client().aclose()


@pytest.mark.asyncio
async def test_async_get_drive_gives_up_after_budget():
    inner = _CountingAsyncTransport([502])
    client = _client_with_async_transport(inner, retries=1)

    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        await get_drive.asyncio(drive_name="test-drive", client=client)

    assert exc_info.value.status_code == 502
    assert inner.methods == ["GET", "GET"]
    await client.get_async_httpx_client().aclose()
