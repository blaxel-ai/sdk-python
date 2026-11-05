"""Tests for tools functionality."""

import pytest
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData

from blaxel.core.tools import (
    MCP_SESSION_TERMINATED_CODE,
    PersistentMcpClient,
    bl_tools,
    is_session_terminated_error,
)


def _session_terminated_error() -> McpError:
    return McpError(ErrorData(code=MCP_SESSION_TERMINATED_CODE, message="Session terminated"))


@pytest.mark.asyncio
async def test_bl_tools_creation():
    """Test tools creation."""
    tools = bl_tools(["blaxel-search"])
    assert tools.functions == ["blaxel-search"]
    assert tools.metas == {}
    assert tools.timeout == 1  # DEFAULT_TIMEOUT
    assert tools.timeout_enabled is True


@pytest.mark.asyncio
async def test_bl_tools_with_metas():
    """Test tools creation with metadata."""
    metas = {"test": "value", "env": "testing"}
    tools = bl_tools(["blaxel-search"], metas=metas)
    assert tools.metas == metas


@pytest.mark.asyncio
async def test_bl_tools_with_timeout():
    """Test tools creation with custom timeout."""
    tools = bl_tools(["blaxel-search"], timeout=10, timeout_enabled=False)
    assert tools.timeout == 10
    assert tools.timeout_enabled is False


@pytest.mark.asyncio
async def test_bl_tools_framework_conversions():
    """Test tools framework conversions."""
    tools = bl_tools(["blaxel-search"])

    # Test that conversion methods would exist after initialization
    # (These require actual MCP server connections to test fully)
    assert hasattr(tools, "get_tools")


@pytest.mark.asyncio
async def test_bl_tools_core_methods():
    """Test tools core methods."""
    tools = bl_tools(["blaxel-search"])

    # Test that core methods exist
    assert hasattr(tools, "get_tools")
    assert hasattr(tools, "initialize")
    assert hasattr(tools, "connect")


@pytest.mark.asyncio
async def test_bl_tools_multiple_functions():
    """Test tools with multiple functions."""
    functions = ["blaxel-search", "function-2", "function-3"]
    tools = bl_tools(functions)
    assert tools.functions == functions


@pytest.mark.asyncio
async def test_bl_tools_default_timeout():
    """Test default timeout value."""
    from blaxel.core.tools import DEFAULT_TIMEOUT

    tools = bl_tools(["test"])
    assert tools.timeout == DEFAULT_TIMEOUT


def test_is_session_terminated_error_matches_mcp_code():
    """The real McpError (code 32600) raised by the transport is detected."""
    assert is_session_terminated_error(_session_terminated_error())


class _FakeExceptionGroup(Exception):
    """Mirrors the ``.exceptions`` attribute of anyio/PEP 654 exception groups.

    Defined explicitly rather than using the ``ExceptionGroup`` builtin so the
    test stays valid on the SDK's minimum supported Python (3.10).
    """

    def __init__(self, message: str, exceptions: list[BaseException]):
        super().__init__(message)
        self.exceptions = exceptions


def test_is_session_terminated_error_matches_when_wrapped():
    """Detection walks the cause chain and exception groups."""
    wrapped = RuntimeError("tool failed")
    wrapped.__cause__ = _session_terminated_error()
    assert is_session_terminated_error(wrapped)

    group = _FakeExceptionGroup("boom", [ValueError("x"), _session_terminated_error()])
    assert is_session_terminated_error(group)


def test_is_session_terminated_error_ignores_other_errors():
    """Unrelated failures must not trigger the reconnect path."""
    assert not is_session_terminated_error(RuntimeError("boom"))
    assert not is_session_terminated_error(
        McpError(ErrorData(code=-32000, message="Internal error"))
    )


class _FakeSession:
    """Minimal ClientSession stand-in: fail once, then succeed."""

    def __init__(self, error: BaseException, success):
        self._error = error
        self._success = success
        self.send_request_calls = 0
        self.list_tools_calls = 0

    async def send_request(self, _request, _result_type):
        self.send_request_calls += 1
        if self.send_request_calls == 1:
            raise self._error
        return self._success

    async def list_tools(self):
        self.list_tools_calls += 1
        if self.list_tools_calls == 1:
            raise self._error
        return self._success


class _ListResult:
    def __init__(self, tools):
        self.tools = tools


def _wire_fake_client(monkeypatch, session: _FakeSession) -> dict:
    """Build a PersistentMcpClient whose session lifecycle is fully stubbed."""
    client = PersistentMcpClient("test-function", timeout_enabled=False)
    state = {"initialized": 0, "closed": 0}

    async def fake_initialize():
        state["initialized"] += 1
        client.session = session

    async def fake_close():
        state["closed"] += 1
        client.session = None

    monkeypatch.setattr(client, "initialize", fake_initialize)
    monkeypatch.setattr(client, "_close", fake_close)
    return {"client": client, "state": state}


@pytest.mark.asyncio
async def test_call_tool_reconnects_on_session_terminated(monkeypatch):
    """A server-terminated session is torn down and the call retried once."""
    from mcp.types import CallToolResult

    success = CallToolResult(content=[{"type": "text", "text": "ok"}], isError=False)
    session = _FakeSession(_session_terminated_error(), success)
    wired = _wire_fake_client(monkeypatch, session)
    client, state = wired["client"], wired["state"]

    result = await client.call_tool("ListInvestorUpdatesByStatus", {})

    assert result.isError is False
    assert session.send_request_calls == 2  # failed once, retried once
    assert state["initialized"] == 2  # initial + reconnect
    assert state["closed"] >= 1  # stale session was disposed


@pytest.mark.asyncio
async def test_call_tool_does_not_retry_other_errors(monkeypatch):
    """Non-terminated errors keep the existing swallow-and-report behavior."""
    session = _FakeSession(RuntimeError("boom"), None)
    wired = _wire_fake_client(monkeypatch, session)
    client, state = wired["client"], wired["state"]

    result = await client.call_tool("ListInvestorUpdatesByStatus", {})

    assert result.isError is True
    assert session.send_request_calls == 1  # no retry
    assert state["initialized"] == 1  # no reconnect


@pytest.mark.asyncio
async def test_list_tools_reconnects_on_session_terminated(monkeypatch):
    """list_tools recovers from a terminated session and retries once."""
    expected = _ListResult(["tool-a", "tool-b"])
    session = _FakeSession(_session_terminated_error(), expected)
    wired = _wire_fake_client(monkeypatch, session)
    client, state = wired["client"], wired["state"]

    result = await client.list_tools()

    assert result is expected
    assert client.tools_cache == ["tool-a", "tool-b"]
    assert session.list_tools_calls == 2
    assert state["initialized"] == 2


@pytest.mark.asyncio
async def test_list_tools_reraises_other_errors(monkeypatch):
    """list_tools still propagates unrelated errors (unchanged behavior)."""
    session = _FakeSession(RuntimeError("boom"), None)
    wired = _wire_fake_client(monkeypatch, session)
    client, state = wired["client"], wired["state"]

    with pytest.raises(RuntimeError, match="boom"):
        await client.list_tools()
    assert session.list_tools_calls == 1
    assert state["initialized"] == 1
