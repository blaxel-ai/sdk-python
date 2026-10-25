"""Tests for PersistentMcpClient connection-failure handling.

These cover the fix for the anyio task-group leak that surfaced in telemetry as
``ExceptionGroup: unhandled errors in a TaskGroup``: when an MCP server is
unreachable or returns an error status (common while a server cold-starts), the
streamable-HTTP transport's anyio task group used to leak an un-catchable
exception group / CancelledError to the caller and leave a dangling task group
that the asyncio exception handler reported. The client now owns the whole
transport lifecycle in a single task and surfaces a concrete, catchable error.
"""

import asyncio
import socket
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from blaxel.core.common.settings import settings
from blaxel.core.tools import (
    BlTools,
    PersistentMcpClient,
    _as_connection_error,
    _flatten_exception_group,
    toolPersistances,
)

try:  # (Base)ExceptionGroup are builtins on 3.11+, backported on 3.10.
    _ExceptionGroup = ExceptionGroup
    _BaseExceptionGroup = BaseExceptionGroup
except NameError:  # pragma: no cover - only on Python 3.10
    from exceptiongroup import BaseExceptionGroup as _BaseExceptionGroup
    from exceptiongroup import ExceptionGroup as _ExceptionGroup


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _no_auth_headers(monkeypatch):
    """Avoid real credentials: the transport only needs some headers dict."""
    monkeypatch.setattr(type(settings), "headers", property(lambda self: {}), raising=False)
    yield
    toolPersistances.clear()


class _ErrorHandler(BaseHTTPRequestHandler):
    status = 503

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(length)
        self.send_response(self.status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"error":"unavailable"}')

    def do_GET(self):
        self.send_response(self.status)
        self.end_headers()

    def log_message(self, *args):  # silence test server
        pass


@contextmanager
def error_status_server(status=503):
    """Run a local HTTP server that answers every request with ``status``."""
    _ErrorHandler.status = status
    server = HTTPServer(("127.0.0.1", 0), _ErrorHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        server.server_close()


def closed_port_url():
    """Return a URL whose port is guaranteed to refuse connections."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return f"http://127.0.0.1:{port}"


def _client_for(url: str, **kwargs) -> PersistentMcpClient:
    client = PersistentMcpClient("myfunc", **kwargs)

    async def _resolve_url(_self=client):
        return url

    client._resolve_url = _resolve_url  # type: ignore[method-assign]
    return client


@contextmanager
def recording_loop_exceptions():
    """Capture exceptions reported to the running loop's exception handler.

    A dangling anyio task group surfaces here (and, in production, is forwarded to
    Sentry). The fix must leave this empty.
    """
    loop = asyncio.get_running_loop()
    recorded: list = []
    previous = loop.get_exception_handler()

    def handler(_loop, context):
        recorded.append(context.get("exception") or context.get("message"))

    loop.set_exception_handler(handler)
    try:
        yield recorded
    finally:
        loop.set_exception_handler(previous)


# ---------------------------------------------------------------------------
# Unit tests for the exception-group helpers
# ---------------------------------------------------------------------------
def test_flatten_exception_group_returns_single_leaf():
    leaf = ConnectionError("refused")
    group = _ExceptionGroup("task group", [leaf])
    assert _flatten_exception_group(group) is leaf


def test_flatten_exception_group_strips_cancellations():
    leaf = ValueError("boom")
    # A CancelledError is a BaseException, so the group is a BaseExceptionGroup.
    group = _BaseExceptionGroup("task group", [asyncio.CancelledError(), leaf])
    assert _flatten_exception_group(group) is leaf


def test_flatten_exception_group_keeps_multiple_leaves():
    group = _ExceptionGroup("task group", [ValueError("a"), KeyError("b")])
    assert _flatten_exception_group(group) is group


def test_flatten_exception_group_unwraps_nested():
    leaf = TimeoutError("slow")
    group = _ExceptionGroup("outer", [_ExceptionGroup("inner", [leaf])])
    assert _flatten_exception_group(group) is leaf


def test_flatten_non_group_passthrough():
    err = ValueError("plain")
    assert _flatten_exception_group(err) is err


def test_as_connection_error_unwraps_to_concrete():
    leaf = ConnectionError("refused")
    group = _ExceptionGroup("task group", [leaf])
    assert _as_connection_error("myfunc", group) is leaf


def test_as_connection_error_wraps_non_exception():
    # A bare cancellation is not catchable via ``except Exception``; it must be
    # wrapped so callers always receive an Exception.
    result = _as_connection_error("myfunc", asyncio.CancelledError())
    assert isinstance(result, Exception)
    assert not isinstance(result, asyncio.CancelledError)
    assert "myfunc" in str(result)


# ---------------------------------------------------------------------------
# Error-path integration tests (local transport, no credentials)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("timeout_enabled", [True, False])
async def test_initialize_error_status_raises_catchable(timeout_enabled):
    with error_status_server(503) as url:
        client = _client_for(url, timeout_enabled=timeout_enabled)
        with recording_loop_exceptions() as recorded:
            with pytest.raises(Exception) as exc_info:  # noqa: PT011
                await asyncio.wait_for(client.initialize(), timeout=20)
            # Must NOT be an un-catchable BaseException (CancelledError/ExceptionGroup).
            assert not isinstance(exc_info.value, asyncio.CancelledError)
            assert not isinstance(exc_info.value, _BaseExceptionGroup)
            assert client.session is None
            await asyncio.sleep(0.2)
        assert recorded == [], f"dangling loop exceptions: {recorded}"


@pytest.mark.parametrize("timeout_enabled", [True, False])
async def test_initialize_connection_refused_raises_catchable(timeout_enabled):
    url = closed_port_url()
    client = _client_for(url, timeout_enabled=timeout_enabled)
    with recording_loop_exceptions() as recorded:
        with pytest.raises(Exception) as exc_info:  # noqa: PT011
            await asyncio.wait_for(client.initialize(), timeout=20)
        assert not isinstance(exc_info.value, asyncio.CancelledError)
        assert not isinstance(exc_info.value, _BaseExceptionGroup)
        assert client.session is None
        await asyncio.sleep(0.2)
    assert recorded == [], f"dangling loop exceptions: {recorded}"


async def test_list_tools_connection_error_is_catchable():
    with error_status_server(503) as url:
        client = _client_for(url, timeout_enabled=False)
        with pytest.raises(Exception) as exc_info:  # noqa: PT011
            await asyncio.wait_for(client.list_tools(), timeout=20)
        assert not isinstance(exc_info.value, asyncio.CancelledError)


async def test_bl_tools_initialize_surfaces_catchable_error(monkeypatch):
    """The gather/connect path in BlTools.initialize must also stay catchable."""
    with error_status_server(503) as url:

        async def _resolve_url(self):
            return url

        monkeypatch.setattr(PersistentMcpClient, "_resolve_url", _resolve_url)
        tools = BlTools(["myfunc"], timeout_enabled=False)
        with recording_loop_exceptions() as recorded:
            with pytest.raises(Exception) as exc_info:  # noqa: PT011
                await asyncio.wait_for(tools.initialize(), timeout=20)
            assert not isinstance(exc_info.value, asyncio.CancelledError)
            await asyncio.sleep(0.2)
        assert recorded == [], f"dangling loop exceptions: {recorded}"


# ---------------------------------------------------------------------------
# Happy-path regression test against a real streamable-HTTP MCP server
# ---------------------------------------------------------------------------
def _start_fastmcp_server():
    pytest.importorskip("uvicorn")
    fastmcp_mod = pytest.importorskip("mcp.server.fastmcp")

    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    server = fastmcp_mod.FastMCP(name="test-mcp", host="127.0.0.1", port=port, log_level="ERROR")

    @server.tool()
    def echo(text: str) -> str:
        return f"echo: {text}"

    thread = threading.Thread(target=lambda: server.run(transport="streamable-http"), daemon=True)
    thread.start()
    for _ in range(100):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return port
        except OSError:
            threading.Event().wait(0.1)
    pytest.skip("local MCP server did not start")


async def test_happy_path_initialize_list_and_call_and_reconnect():
    port = _start_fastmcp_server()
    with recording_loop_exceptions() as recorded:
        client = _client_for(f"http://127.0.0.1:{port}", timeout=1, timeout_enabled=True)
        result = await client.list_tools()
        assert "echo" in [t.name for t in result.tools]

        call = await client.call_tool("echo", {"text": "hello"})
        assert call.isError is False
        assert call.content[0].text == "echo: hello"

        # Inactivity timer closes the connection; the next call must reconnect.
        await asyncio.sleep(1.5)
        assert client.session is None
        again = await client.call_tool("echo", {"text": "again"})
        assert again.content[0].text == "echo: again"

        await client._close()
        assert client.session is None
        await asyncio.sleep(0.3)
    assert recorded == [], f"dangling loop exceptions: {recorded}"
