"""Tests for tools functionality."""

import pytest
from mcp.shared.exceptions import McpError
from mcp.types import CallToolResult, ErrorData, ListToolsResult, TextContent
from mcp.types import Tool as MCPTool

from blaxel.core.tools import (
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


# --- Session-terminated reconnect handling -------------------------------------


def _session_terminated_error() -> McpError:
    """Build the exact error the MCP transport raises when the server dropped
    the session (a 404 mapped to ``ErrorData`` code 32600)."""
    return McpError(ErrorData(code=32600, message="Session terminated"))


class _FakeSession:
    """A ClientSession stand-in whose calls follow a scripted behavior list."""

    def __init__(self, behavior):
        self._behavior = list(behavior)
        self.calls = 0

    async def list_tools(self):
        return self._next()

    async def send_request(self, *args, **kwargs):
        return self._next()

    def _next(self):
        item = self._behavior[min(self.calls, len(self._behavior) - 1)]
        self.calls += 1
        if isinstance(item, BaseException):
            raise item
        return item


def _client_with_sessions(sessions):
    """A PersistentMcpClient whose initialize() installs each fake session in
    turn, so a reconnect (session discarded -> re-initialize) lands on the next
    scripted session. No real transport is opened."""
    client = PersistentMcpClient("fn", timeout=60, timeout_enabled=False)
    pending = list(sessions)

    async def fake_initialize():
        if client.session is None and pending:
            client.session = pending.pop(0)

    client.initialize = fake_initialize
    return client


def test_is_session_terminated_error():
    assert _is_session_terminated_error(_session_terminated_error()) is True
    # Message match is case/whitespace tolerant.
    assert (
        _is_session_terminated_error(McpError(ErrorData(code=1, message=" Session Terminated ")))
        is True
    )
    assert _is_session_terminated_error(McpError(ErrorData(code=1, message="other error"))) is False
    # A non-McpError carrying the same text must not be treated as terminated.
    assert _is_session_terminated_error(ValueError("Session terminated")) is False


@pytest.mark.asyncio
async def test_list_tools_reconnects_on_session_terminated():
    good = ListToolsResult(
        tools=[MCPTool(name="echo", description="", inputSchema={"type": "object"})]
    )
    dead = _FakeSession([_session_terminated_error()])
    healthy = _FakeSession([good])
    client = _client_with_sessions([dead, healthy])

    result = await client.list_tools()

    assert [t.name for t in result.tools] == ["echo"]
    assert dead.calls == 1  # first (dropped) session was tried once
    assert healthy.calls == 1  # reconnected and retried on a fresh session


@pytest.mark.asyncio
async def test_call_tool_reconnects_on_session_terminated():
    ok = CallToolResult(content=[TextContent(type="text", text="ok")], isError=False)
    dead = _FakeSession([_session_terminated_error()])
    healthy = _FakeSession([ok])
    client = _client_with_sessions([dead, healthy])

    result = await client.call_tool("echo", {"msg": "hi"})

    assert result.isError is not True
    assert dead.calls == 1
    assert healthy.calls == 1


@pytest.mark.asyncio
async def test_list_tools_raises_when_reconnect_keeps_failing():
    # A permanently unavailable server: even the reconnect gets terminated, so
    # the error surfaces instead of being masked -- but only after one retry.
    dead1 = _FakeSession([_session_terminated_error()])
    dead2 = _FakeSession([_session_terminated_error()])
    client = _client_with_sessions([dead1, dead2])

    with pytest.raises(McpError):
        await client.list_tools()

    assert dead1.calls == 1
    assert dead2.calls == 1  # exactly one reconnect, no unbounded looping


@pytest.mark.asyncio
async def test_call_tool_non_terminated_error_is_not_retried():
    dead = _FakeSession([ValueError("boom")])
    client = _client_with_sessions([dead])

    result = await client.call_tool("echo", {})

    # call_tool converts unrecoverable errors into an isError result...
    assert result.isError is True
    # ...and a non-terminated error must not trigger a reconnect.
    assert dead.calls == 1
