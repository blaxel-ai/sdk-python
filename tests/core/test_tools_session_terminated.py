"""Tests for persistent MCP client recovery from a terminated session.

A persistent MCP session can be evicted server-side (server restart,
scale-down, idle-session expiry). The streamable-HTTP transport then receives a
404 for the next request on that session and surfaces it as
``McpError('Session terminated')``. ``PersistentMcpClient`` must drop the stale
session, reconnect, and retry the request once instead of failing the call and
leaving a dead session behind.
"""

import pytest
from mcp.shared.exceptions import McpError
from mcp.types import CallToolResult, ErrorData, ListToolsResult, TextContent

import blaxel.core.tools as tools_mod
from blaxel.core.tools import PersistentMcpClient, _is_session_terminated_error


def _mcp_error(message: str, code: int = 32600) -> McpError:
    return McpError(ErrorData(code=code, message=message))


def _raiser(exc: BaseException):
    def _f():
        raise exc

    return _f


def _ok_call():
    return CallToolResult(content=[TextContent(type="text", text="ok")], isError=False)


def _ok_list():
    return ListToolsResult(tools=[])


def _make_fake_session_class(behaviors):
    """Build a fake ``ClientSession`` whose nth constructed instance runs
    ``behaviors[n]`` (a zero-arg callable that returns a value or raises) for
    both ``send_request`` and ``list_tools``. Returns the class plus the list of
    created instances so tests can assert how many sessions were established.
    """
    created = []

    class _FakeSession:
        def __init__(self, read, write):
            self.index = len(created)
            self.closed = False
            self.initialized = False
            created.append(self)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            self.closed = True
            return False

        async def initialize(self):
            self.initialized = True

        async def send_request(self, request, result_type):
            return behaviors[self.index]()

        async def list_tools(self):
            return behaviors[self.index]()

    return _FakeSession, created


def _patch_client(client, fake_cls, monkeypatch):
    async def fake_resolve():
        return "http://fake"

    async def fake_transport():
        return (object(), object())

    client._resolve_url = fake_resolve
    client._get_transport = fake_transport
    monkeypatch.setattr(tools_mod, "ClientSession", fake_cls)


def test_is_session_terminated_error_detects_terminated():
    assert _is_session_terminated_error(_mcp_error("Session terminated")) is True
    # Match is case-insensitive and substring-based.
    assert _is_session_terminated_error(_mcp_error("SESSION TERMINATED")) is True
    assert _is_session_terminated_error(_mcp_error("the session terminated early")) is True


def test_is_session_terminated_error_ignores_other_errors():
    assert _is_session_terminated_error(_mcp_error("Method not found", code=-32601)) is False
    assert _is_session_terminated_error(ValueError("Session terminated")) is False
    assert _is_session_terminated_error(RuntimeError("boom")) is False


@pytest.mark.asyncio
async def test_call_tool_reconnects_after_session_terminated(monkeypatch):
    fake_cls, created = _make_fake_session_class(
        [_raiser(_mcp_error("Session terminated")), _ok_call]
    )
    client = PersistentMcpClient("fn", timeout_enabled=False)
    _patch_client(client, fake_cls, monkeypatch)

    result = await client.call_tool("do", {})

    assert result.isError is False
    # A fresh session was established (reconnect happened) ...
    assert len(created) == 2
    # ... and the stale session was closed.
    assert created[0].closed is True


@pytest.mark.asyncio
async def test_call_tool_does_not_reconnect_on_unrelated_error(monkeypatch):
    fake_cls, created = _make_fake_session_class(
        [_raiser(_mcp_error("Method not found", code=-32601))]
    )
    client = PersistentMcpClient("fn", timeout_enabled=False)
    _patch_client(client, fake_cls, monkeypatch)

    result = await client.call_tool("do", {})

    # The error is surfaced to the caller without a reconnect attempt.
    assert result.isError is True
    assert len(created) == 1


@pytest.mark.asyncio
async def test_list_tools_reconnects_after_session_terminated(monkeypatch):
    fake_cls, created = _make_fake_session_class(
        [_raiser(_mcp_error("Session terminated")), _ok_list]
    )
    client = PersistentMcpClient("fn", timeout_enabled=False)
    _patch_client(client, fake_cls, monkeypatch)

    result = await client.list_tools()

    assert isinstance(result, ListToolsResult)
    assert len(created) == 2
    assert created[0].closed is True


@pytest.mark.asyncio
async def test_list_tools_propagates_unrelated_error(monkeypatch):
    fake_cls, created = _make_fake_session_class(
        [_raiser(_mcp_error("Method not found", code=-32601))]
    )
    client = PersistentMcpClient("fn", timeout_enabled=False)
    _patch_client(client, fake_cls, monkeypatch)

    with pytest.raises(McpError):
        await client.list_tools()

    assert len(created) == 1


@pytest.mark.asyncio
async def test_call_tool_surfaces_error_when_reconnect_still_terminated(monkeypatch):
    # A persistent 404 (server genuinely gone) must still surface after one
    # retry rather than looping forever.
    fake_cls, created = _make_fake_session_class(
        [_raiser(_mcp_error("Session terminated")), _raiser(_mcp_error("Session terminated"))]
    )
    client = PersistentMcpClient("fn", timeout_enabled=False)
    _patch_client(client, fake_cls, monkeypatch)

    result = await client.call_tool("do", {})

    assert result.isError is True
    # Exactly one reconnect was attempted (2 sessions), not an unbounded loop.
    assert len(created) == 2
