"""Tests for agents functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.agents import bl_agent


@pytest.mark.asyncio
async def test_bl_agent_creation():
    """Test agent creation."""
    agent = bl_agent("test-agent")
    assert agent.name == "test-agent"
    assert str(agent) == "Agent test-agent"


@pytest.mark.asyncio
async def test_bl_agent_url_properties():
    """Test agent URL properties."""
    agent = bl_agent("template-google-adk-py")

    # Test that URL properties are accessible
    assert hasattr(agent, "url")
    assert hasattr(agent, "external_url")
    assert hasattr(agent, "internal_url")
    assert hasattr(agent, "forced_url")
    assert hasattr(agent, "fallback_url")


@pytest.mark.asyncio
@patch("blaxel.core.agents.client")
async def test_bl_agent_run(mock_client):
    """Test agent run functionality."""
    # Mock the HTTP client properly
    mock_httpx_client = MagicMock()
    mock_async_httpx_client = MagicMock()

    # Mock sync response
    mock_sync_response = MagicMock()
    mock_sync_response.status_code = 200
    mock_sync_response.text = "Hello, world!"
    mock_httpx_client.post.return_value = mock_sync_response

    # Mock async response
    mock_async_response = MagicMock()
    mock_async_response.status_code = 200
    mock_async_response.text = "Hello, world!"
    mock_async_httpx_client.post = AsyncMock(return_value=mock_async_response)

    mock_client.get_httpx_client.return_value = mock_httpx_client
    mock_client.get_async_httpx_client.return_value = mock_async_httpx_client

    agent = bl_agent("test-agent")

    # Test sync run
    result = agent.run({"inputs": "Hello, world!"})
    assert result == "Hello, world!"

    # Test async run
    result = await agent.arun({"inputs": "Hello, world!"})
    assert result == "Hello, world!"


@pytest.mark.asyncio
async def test_bl_agent_methods():
    """Test agent has required methods."""
    agent = bl_agent("test-agent")

    # Test that core methods exist
    assert hasattr(agent, "run")
    assert hasattr(agent, "arun")
    assert hasattr(agent, "call")
    assert hasattr(agent, "acall")


@pytest.mark.asyncio
async def test_bl_agent_representation():
    """Test agent string representation."""
    agent = bl_agent("test-agent")

    # Test string representation
    assert str(agent) == "Agent test-agent"
    assert repr(agent) == "Agent test-agent"
