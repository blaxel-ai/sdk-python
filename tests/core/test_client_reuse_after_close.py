"""Regression tests for reusing a ``Client`` after its context manager exits.

``async with client:`` (and ``with client:``) closes the underlying httpx
client. The ``Client`` wrapper caches that httpx client, so if exiting the
context left the closed client cached, the next request reused it and httpx
raised ``RuntimeError: Cannot send a request, as the client has been closed.``
(Sentry SDK-PYTHON-12X). Exiting the context must drop the cached client so a
later call rebuilds a fresh one on the same event loop.
"""

import httpx

from blaxel.core.client.client import Client as ControlplaneClient
from blaxel.core.sandbox.client.client import Client as SandboxClient

BASE_URL = "http://test"


def _handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"ok": True})


def _client(client_cls):
    return client_cls(
        base_url=BASE_URL,
        headers={},
        httpx_args={"transport": httpx.MockTransport(_handler)},
    )


async def _assert_async_reusable(client_cls) -> None:
    client = _client(client_cls)

    async with client:
        first = client.get_async_httpx_client()
        assert (await first.get("/")).status_code == 200

    # The context exit must not leave the closed client cached.
    assert client._async_client is None

    rebuilt = client.get_async_httpx_client()
    assert rebuilt is not first
    assert (await rebuilt.get("/")).status_code == 200


def _assert_sync_reusable(client_cls) -> None:
    client = _client(client_cls)

    with client:
        first = client.get_httpx_client()
        assert first.get("/").status_code == 200

    assert client._client is None

    rebuilt = client.get_httpx_client()
    assert rebuilt is not first
    assert rebuilt.get("/").status_code == 200


async def test_controlplane_async_client_reusable_after_aexit():
    await _assert_async_reusable(ControlplaneClient)


async def test_sandbox_async_client_reusable_after_aexit():
    await _assert_async_reusable(SandboxClient)


def test_controlplane_sync_client_reusable_after_exit():
    _assert_sync_reusable(ControlplaneClient)


def test_sandbox_sync_client_reusable_after_exit():
    _assert_sync_reusable(SandboxClient)


async def test_repeated_async_context_entries_each_issue_requests():
    """Entering/exiting the context repeatedly keeps working, not just once."""
    client = _client(ControlplaneClient)
    for _ in range(3):
        async with client:
            assert (await client.get_async_httpx_client().get("/")).status_code == 200
