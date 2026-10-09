"""Tests for the MCP WebSocket client transport (``blaxel.core.mcp.client``).

Regression coverage for SDK-PYTHON-126: a failing task inside the anyio task group
used to leak an opaque ``BaseExceptionGroup`` ("unhandled errors in a TaskGroup")
out of ``websocket_client`` instead of a concrete, catchable error.
"""

import asyncio
import socket
import sys

import anyio
import pytest
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage, JSONRPCRequest
from websockets.asyncio.server import serve

from blaxel.core.mcp.client import _single_task_group_error, websocket_client

if sys.version_info < (3, 11):
    from exceptiongroup import BaseExceptionGroup


def _closed_port() -> int:
    """Bind then release a port so a connection to it is refused deterministically."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.mark.asyncio
async def test_connection_failure_does_not_leak_exception_group():
    """A refused connection must surface as a concrete, catchable error."""
    url = f"http://127.0.0.1:{_closed_port()}"

    with pytest.raises(OSError) as exc_info:
        async with websocket_client(url, timeout=2) as (_read, _write):
            pass

    # The opaque task-group group must not leak out.
    assert not isinstance(exc_info.value, BaseExceptionGroup)


@pytest.mark.asyncio
async def test_connection_failure_caught_by_plain_except():
    """Callers using ordinary ``except OSError`` handling must catch the failure."""
    url = f"http://127.0.0.1:{_closed_port()}"

    caught = None
    try:
        async with websocket_client(url, timeout=2) as (_read, _write):
            pass
    except OSError as exc:  # ConnectionRefusedError is an OSError subclass
        caught = exc
    assert caught is not None


@pytest.mark.asyncio
async def test_happy_path_roundtrip_exits_cleanly():
    """A successful connect / send / exit must not raise or leak an exception group."""
    received: list[str] = []

    async def handler(websocket):
        try:
            async for raw in websocket:
                received.append(raw)
        except Exception:
            pass

    async with serve(handler, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        url = f"http://127.0.0.1:{port}"
        async with websocket_client(url, timeout=5) as (_read_stream, write_stream):
            message = SessionMessage(
                message=JSONRPCMessage(root=JSONRPCRequest(jsonrpc="2.0", id=1, method="ping"))
            )
            await write_stream.send(message)
            await anyio.sleep(0.2)

    assert len(received) == 1


@pytest.mark.asyncio
async def test_single_task_group_error_returns_lone_exception():
    group = BaseExceptionGroup("boom", [ValueError("boom")])
    result = _single_task_group_error(group)
    assert isinstance(result, ValueError)


@pytest.mark.asyncio
async def test_single_task_group_error_strips_cancellation():
    group = BaseExceptionGroup("mixed", [asyncio.CancelledError(), ValueError("boom")])
    result = _single_task_group_error(group)
    assert isinstance(result, ValueError)


@pytest.mark.asyncio
async def test_single_task_group_error_cancellation_only_is_none():
    group = BaseExceptionGroup("cancelled", [asyncio.CancelledError()])
    assert _single_task_group_error(group) is None


@pytest.mark.asyncio
async def test_single_task_group_error_unwraps_nested_group():
    group = BaseExceptionGroup("outer", [BaseExceptionGroup("inner", [ValueError("boom")])])
    result = _single_task_group_error(group)
    assert isinstance(result, ValueError)


@pytest.mark.asyncio
async def test_single_task_group_error_keeps_group_for_multiple_errors():
    group = BaseExceptionGroup("multi", [ValueError("a"), KeyError("b")])
    result = _single_task_group_error(group)
    assert isinstance(result, BaseExceptionGroup)
    assert len(result.exceptions) == 2
