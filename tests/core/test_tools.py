"""Tests for tools functionality."""

from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core.tools import bl_tools


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
async def test_bl_tools_url_methods():
    """Test tools URL generation methods."""
    tools = bl_tools(["test-function"])

    # Test URL methods exist
    assert hasattr(tools, "_url")
    assert hasattr(tools, "_forced_url")
    assert hasattr(tools, "_external_url")
    assert hasattr(tools, "_internal_url")
    assert hasattr(tools, "_fallback_url")


@pytest.mark.asyncio
@patch("blaxel.core.tools.websocket_client")
async def test_bl_tools_framework_conversions(mock_websocket):
    """Test tools framework conversions."""
    # Mock websocket and tools
    mock_session = AsyncMock()
    mock_session.list_tools.return_value.tools = []

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
    assert hasattr(tools, "connect_with_url")


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
