"""Regression tests for PersistentMcpClient.initialize() connection retries.

The retry loop guards against transient MCP connection failures that happen
while a function/sandbox is still cold-starting (e.g. the gateway answers a
handshake with a plain HTTP response instead of upgrading, or the stream
resets). Without it, a cold start surfaces as an uncaught exception
(see Sentry SDK-PYTHON-125). The retry was added in #119 and accidentally
reverted by an unrelated drives PR (#117); these tests lock the behavior in.
"""

import pytest

from blaxel.core.tools import PersistentMcpClient


class FakeClientSession:
    """Minimal async-context-manager stand-in for mcp.ClientSession."""

    def __init__(self, read, write):
        self.read = read
        self.write = write
        self.initialized = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def initialize(self):
        self.initialized = True


@pytest.fixture
def patched_session(monkeypatch):
    monkeypatch.setattr("blaxel.core.tools.ClientSession", FakeClientSession)


def _make_client() -> PersistentMcpClient:
    client = PersistentMcpClient("test-fn")

    async def _resolve_url():
        return "https://example.test"

    # Avoid any control-plane / network lookup during the test.
    client._resolve_url = _resolve_url  # type: ignore[method-assign]
    return client


@pytest.mark.asyncio
async def test_initialize_retries_until_transport_succeeds(patched_session):
    attempts = {"n": 0}

    async def flaky_transport():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError("server rejected connection while cold starting")
        return object(), object()

    client = _make_client()
    client._get_transport = flaky_transport  # type: ignore[method-assign]

    # retry_delay=0 keeps the test instant.
    await client.initialize(retries=3, retry_delay=0)

    assert attempts["n"] == 3
    assert client.session is not None
    assert client.session.initialized is True


@pytest.mark.asyncio
async def test_initialize_raises_last_error_after_exhausting_retries(patched_session):
    attempts = {"n": 0}

    async def always_fail():
        attempts["n"] += 1
        raise RuntimeError("still booting")

    client = _make_client()
    client._get_transport = always_fail  # type: ignore[method-assign]

    with pytest.raises(RuntimeError, match="still booting"):
        await client.initialize(retries=2, retry_delay=0)

    # Initial attempt + 2 retries.
    assert attempts["n"] == 3
    assert client.session is None


@pytest.mark.asyncio
async def test_initialize_is_noop_when_already_connected(patched_session):
    called = {"transport": False}

    async def should_not_run():
        called["transport"] = True
        return object(), object()

    client = _make_client()
    client._get_transport = should_not_run  # type: ignore[method-assign]
    client.session = object()  # type: ignore[assignment]

    await client.initialize(retries=3, retry_delay=0)

    assert called["transport"] is False
