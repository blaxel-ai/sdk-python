"""Tests for the MCP WebSocket server transport (``blaxel.core.mcp.server``).

Regression coverage for SDK-PYTHON-12J: a failing child task (or body error) inside
the anyio task group used by ``BlaxelMcpServerTransport.websocket_server`` leaked an
opaque ``BaseExceptionGroup`` ("unhandled errors in a TaskGroup") out of
``run_ws_async`` to the process boundary instead of a concrete, catchable error. In
addition, a single unserializable outgoing message crashed the whole sender task and
took the server down.
"""

import asyncio
import socket
import sys

import anyio
import pytest
from mcp.shared.message import SessionMessage

from blaxel.core.mcp.server import BlaxelMcpServerTransport, _single_task_group_error

if sys.version_info < (3, 11):
    from exceptiongroup import BaseExceptionGroup


def _free_port() -> int:
    """Bind then release a port so the server can bind it on a fresh socket."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


class _Unserializable:
    """Stand-in for a message whose JSON serialization raises in message_sender."""

    id = None

    def model_dump_json(self, **_kwargs):
        raise RuntimeError("cannot serialize message")


# --- _single_task_group_error unit tests (mirror the client-side helper) ------------


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


# --- websocket_server boundary behavior ---------------------------------------------


@pytest.mark.asyncio
async def test_body_error_surfaces_as_concrete_exception_not_group():
    """A failure while serving must not leak the opaque task-group ExceptionGroup."""
    transport = BlaxelMcpServerTransport(port=_free_port())

    with pytest.raises(ValueError) as exc_info:
        async with transport.websocket_server() as (_read_stream, _write_stream):
            raise ValueError("body failure")

    # The opaque "unhandled errors in a TaskGroup" group must not escape.
    assert not isinstance(exc_info.value, BaseExceptionGroup)
    assert str(exc_info.value) == "body failure"


@pytest.mark.asyncio
async def test_message_sender_survives_unserializable_message():
    """One malformed outgoing message must be skipped, not crash the server loop."""
    transport = BlaxelMcpServerTransport(port=_free_port())

    sends_completed = 0
    # fail_after guards against a regression (a crash would block the second send).
    with anyio.fail_after(10):
        async with transport.websocket_server() as (_read_stream, write_stream):
            await write_stream.send(SessionMessage(message=_Unserializable()))
            sends_completed += 1
            # A buffer-0 send only returns once message_sender has taken the PREVIOUS
            # item off the stream, so the second send returning proves the sender loop
            # survived the first unserializable message instead of crashing.
            await write_stream.send(SessionMessage(message=_Unserializable()))
            sends_completed += 1
            # Close the send side so message_sender's async-for ends and the task group
            # tears down cleanly (the server otherwise runs until cancelled).
            await write_stream.aclose()
            await anyio.sleep(0.1)

    assert sends_completed == 2
