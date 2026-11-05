"""Tests for PersistentMcpClient resilience to terminated / closed MCP sessions.

A persistent MCP client reuses a single session across calls. When the server
terminates that session (e.g. the MCP workload cold-starts and the streamable
HTTP transport answers a request with a 404 -> ``McpError: Session terminated``,
or the transport is closed mid-request -> ``Connection closed``), the client
must drop the dead session so the next call reconnects instead of reusing it
forever. For a session that was terminated before the request was dispatched the
call is also transparently retried once on a fresh session.
"""

import pytest
from mcp.shared.exceptions import McpError
from mcp.types import CallToolResult, ErrorData, ListToolsResult

import blaxel.core.tools as tools_mod
from blaxel.core.tools import PersistentMcpClient


class _FakeSession:
    """Stand-in for an ``mcp.ClientSession`` with scripted behaviors."""

    def __init__(self, call_behaviors=None, list_behaviors=None):
        self._call = list(call_behaviors or [])
        self._list = list(list_behaviors or [])
        self.initialized = False

    async def initialize(self):
        self.initialized = True

    async def send_request(self, *args, **kwargs):
        return self._next(self._call)

    async def list_tools(self):
        return self._next(self._list)

    @staticmethod
    def _next(behaviors):
        if not behaviors:
            raise AssertionError("unexpected extra call on fake session")
        behavior = behaviors.pop(0)
        if isinstance(behavior, BaseException):
            raise behavior
        return behavior


class _FakeSessionCM:
    def __init__(self, session):
        self._session = session

    async def __aenter__(self):
        return self._session

    async def __aexit__(self, *exc):
        return False


def _session_terminated():
    # The mcp streamable-HTTP transport emits this (with the positive 32600 code)
    # when a request receives an HTTP 404 because the session no longer exists.
    return McpError(ErrorData(code=32600, message="Session terminated"))


def _connection_closed():
    return McpError(ErrorData(code=-32000, message="Connection closed"))


def _wire(monkeypatch, sessions):
    """Build a client whose initialize() hands out ``sessions`` in order.

    Returns ``(client, created)`` where ``created`` records each session the
    client actually connected to, so tests can assert on reconnection.
    """
    client = PersistentMcpClient("myfunc", timeout_enabled=False)
    created = []
    session_iter = iter(sessions)

    def fake_client_session(read, write):
        session = next(session_iter)
        created.append(session)
        return _FakeSessionCM(session)

    async def fake_get_transport():
        return (None, None)

    async def fake_resolve_url():
        return "http://fake"

    monkeypatch.setattr(tools_mod, "ClientSession", fake_client_session)
    monkeypatch.setattr(client, "_get_transport", fake_get_transport)
    monkeypatch.setattr(client, "_resolve_url", fake_resolve_url)
    return client, created


@pytest.mark.asyncio
async def test_call_tool_recovers_from_session_terminated(monkeypatch):
    ok = CallToolResult(content=[], isError=False)
    s1 = _FakeSession(call_behaviors=[_session_terminated()])
    s2 = _FakeSession(call_behaviors=[ok])
    client, created = _wire(monkeypatch, [s1, s2])

    result = await client.call_tool("GetAgentPromptByName", {})

    assert result is ok
    assert result.isError is False
    assert len(created) == 2  # dropped the dead session and reconnected


@pytest.mark.asyncio
async def test_call_tool_resets_session_when_retry_also_fails(monkeypatch):
    s1 = _FakeSession(call_behaviors=[_session_terminated()])
    s2 = _FakeSession(call_behaviors=[_session_terminated()])
    client, created = _wire(monkeypatch, [s1, s2])

    result = await client.call_tool("GetAgentPromptByName", {})

    assert result.isError is True  # surfaced as an error result, not raised
    assert len(created) == 2  # retried exactly once
    assert client.session is None  # dead session not left cached for next call


@pytest.mark.asyncio
async def test_call_tool_connection_closed_resets_without_retry(monkeypatch):
    s1 = _FakeSession(call_behaviors=[_connection_closed()])
    client, created = _wire(monkeypatch, [s1])

    result = await client.call_tool("GetAgentPromptByName", {})

    assert result.isError is True
    # Connection closed may have been dispatched, so it is NOT auto-retried...
    assert len(created) == 1
    # ...but the unusable session is still dropped so the next call reconnects.
    assert client.session is None


@pytest.mark.asyncio
async def test_call_tool_keeps_session_on_non_stale_error(monkeypatch):
    s1 = _FakeSession(call_behaviors=[ValueError("boom")])
    client, created = _wire(monkeypatch, [s1])

    result = await client.call_tool("tool", {})

    assert result.isError is True
    assert len(created) == 1  # no reconnect for an unrelated error
    assert client.session is s1  # healthy session preserved


@pytest.mark.asyncio
async def test_list_tools_recovers_from_session_terminated(monkeypatch):
    tools_result = ListToolsResult(tools=[])
    s1 = _FakeSession(list_behaviors=[_session_terminated()])
    s2 = _FakeSession(list_behaviors=[tools_result])
    client, created = _wire(monkeypatch, [s1, s2])

    result = await client.list_tools()

    assert result is tools_result
    assert len(created) == 2


@pytest.mark.asyncio
async def test_list_tools_reraises_non_stale_error(monkeypatch):
    s1 = _FakeSession(list_behaviors=[RuntimeError("down")])
    client, created = _wire(monkeypatch, [s1])

    with pytest.raises(RuntimeError, match="down"):
        await client.list_tools()

    assert len(created) == 1
    assert client.session is s1


def test_classify_session_terminated_by_code():
    assert PersistentMcpClient._is_session_terminated_error(
        McpError(ErrorData(code=32600, message="anything"))
    )
    assert PersistentMcpClient._is_session_terminated_error(
        McpError(ErrorData(code=-32600, message="anything"))
    )


def test_classify_session_terminated_by_message():
    assert PersistentMcpClient._is_session_terminated_error(RuntimeError("Session terminated"))
    assert PersistentMcpClient._is_stale_session_error(RuntimeError("Session terminated"))


def test_connection_closed_is_stale_but_not_terminated():
    exc = _connection_closed()
    assert PersistentMcpClient._is_stale_session_error(exc)
    assert not PersistentMcpClient._is_session_terminated_error(exc)


def test_generic_error_is_not_stale():
    assert not PersistentMcpClient._is_stale_session_error(ValueError("boom"))
    assert not PersistentMcpClient._is_session_terminated_error(ValueError("boom"))
