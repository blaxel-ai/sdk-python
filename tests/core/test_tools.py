"""Tests for tools functionality."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp import McpError
from mcp.types import CallToolResult, ErrorData, ListToolsResult

from blaxel.core.tools import (
    SESSION_TERMINATED_MESSAGE,
    PersistentMcpClient,
    _is_session_terminated_error,
    bl_tools,
)


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


def _session_terminated_error() -> McpError:
    return McpError(ErrorData(code=-32600, message=SESSION_TERMINATED_MESSAGE))


def test_is_session_terminated_error():
    """Only a terminated-session McpError should be treated as recoverable."""
    assert _is_session_terminated_error(_session_terminated_error()) is True
    assert _is_session_terminated_error(McpError(ErrorData(code=-32000, message="boom"))) is False
    assert _is_session_terminated_error(ValueError(SESSION_TERMINATED_MESSAGE)) is False


def _patch_initialize(client, make_session, monkeypatch):
    """Make ``initialize`` lazily build a fresh session, as the real one does.

    Returns the list of sessions created so tests can assert a reconnect
    happened (a new session object is built after the stale one is discarded).
    """
    sessions = []

    async def fake_initialize():
        if client.session is None:
            session = make_session()
            client.session = session
            sessions.append(session)

    monkeypatch.setattr(client, "initialize", fake_initialize)
    return sessions


@pytest.mark.asyncio
async def test_list_tools_reconnects_after_session_terminated(monkeypatch):
    """A terminated cached session is rebuilt and list_tools retries once."""
    client = PersistentMcpClient("fn", timeout_enabled=False)
    calls = {"n": 0}

    def make_session():
        session = MagicMock()

        async def list_tools_side_effect():
            calls["n"] += 1
            if calls["n"] == 1:
                raise _session_terminated_error()
            return ListToolsResult(tools=[])

        session.list_tools = AsyncMock(side_effect=list_tools_side_effect)
        return session

    sessions = _patch_initialize(client, make_session, monkeypatch)

    result = await client.list_tools()

    assert result.tools == []
    assert calls["n"] == 2, "list_tools should retry exactly once after termination"
    assert len(sessions) == 2, "a new session must be established on reconnect"
    assert client.session is None, "session is closed after a timeout-disabled call"


@pytest.mark.asyncio
async def test_list_tools_propagates_non_terminated_errors(monkeypatch):
    """Errors other than a terminated session are not retried or swallowed."""
    client = PersistentMcpClient("fn", timeout_enabled=False)
    calls = {"n": 0}

    def make_session():
        session = MagicMock()

        async def list_tools_side_effect():
            calls["n"] += 1
            raise McpError(ErrorData(code=-32000, message="boom"))

        session.list_tools = AsyncMock(side_effect=list_tools_side_effect)
        return session

    _patch_initialize(client, make_session, monkeypatch)

    with pytest.raises(McpError):
        await client.list_tools()
    assert calls["n"] == 1, "non-terminated errors must not trigger a retry"


@pytest.mark.asyncio
async def test_call_tool_reconnects_after_session_terminated(monkeypatch):
    """A terminated cached session is rebuilt and call_tool retries once."""
    client = PersistentMcpClient("fn", timeout_enabled=False)
    calls = {"n": 0}

    def make_session():
        session = MagicMock()

        async def send_request_side_effect(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise _session_terminated_error()
            return CallToolResult(content=[], isError=False)

        session.send_request = AsyncMock(side_effect=send_request_side_effect)
        return session

    sessions = _patch_initialize(client, make_session, monkeypatch)

    result = await client.call_tool("mytool", {})

    assert result.isError is False
    assert calls["n"] == 2, "call_tool should retry exactly once after termination"
    assert len(sessions) == 2, "a new session must be established on reconnect"
