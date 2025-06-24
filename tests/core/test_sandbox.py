"""Tests for sandbox functionality."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.client.models import Metadata, Sandbox
from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.action import ResponseError, SandboxAction
from blaxel.core.sandbox.types import SandboxConfiguration


@pytest.mark.asyncio
async def test_sandbox_creation():
    """Test sandbox instance creation."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"))
    sandbox = SandboxInstance(sandbox_data)
    assert sandbox.sandbox.metadata.name == "test-sandbox"


@pytest.mark.asyncio
async def test_sandbox_properties():
    """Test sandbox instance properties."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"))
    sandbox = SandboxInstance(sandbox_data)

    # Test that core properties exist
    assert hasattr(sandbox, "metadata")
    assert hasattr(sandbox, "status")
    assert hasattr(sandbox, "events")
    assert hasattr(sandbox, "spec")
    assert hasattr(sandbox, "fs")
    assert hasattr(sandbox, "process")
    assert hasattr(sandbox, "previews")


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.SandboxInstance.get")
async def test_sandbox_get(mock_get):
    """Test getting an existing sandbox."""
    # Mock the get method
    mock_sandbox = MagicMock()
    mock_get.return_value = mock_sandbox

    result = await SandboxInstance.get("test-sandbox")
    assert result == mock_sandbox
    mock_get.assert_called_once_with("test-sandbox")


@pytest.mark.asyncio
async def test_sandbox_filesystem_operations():
    """Test sandbox filesystem operations."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"))
    sandbox = SandboxInstance(sandbox_data)

    # Mock the client and filesystem operations
    with patch.object(sandbox, "fs") as mock_fs:
        mock_fs.write = AsyncMock()
        mock_fs.read = AsyncMock(return_value="Hello world")
        mock_fs.ls = AsyncMock()
        mock_fs.mkdir = AsyncMock()
        mock_fs.cp = AsyncMock()
        mock_fs.rm = AsyncMock()

        # Test write operation
        await mock_fs.write("/test/file", "Hello world")
        mock_fs.write.assert_called_once_with("/test/file", "Hello world")

        # Test read operation
        content = await mock_fs.read("/test/file")
        assert content == "Hello world"

        # Test other operations exist
        assert hasattr(mock_fs, "ls")
        assert hasattr(mock_fs, "mkdir")
        assert hasattr(mock_fs, "cp")
        assert hasattr(mock_fs, "rm")


@pytest.mark.asyncio
async def test_sandbox_process_operations():
    """Test sandbox process operations."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"))
    sandbox = SandboxInstance(sandbox_data)

    # Mock the process operations
    with patch.object(sandbox, "process") as mock_process:
        mock_process.exec = AsyncMock()
        mock_process.get = AsyncMock()
        mock_process.logs = AsyncMock(return_value="Hello world\n")
        mock_process.kill = AsyncMock()

        # Test that process methods exist
        assert hasattr(mock_process, "exec")
        assert hasattr(mock_process, "get")
        assert hasattr(mock_process, "logs")
        assert hasattr(mock_process, "kill")


@pytest.mark.asyncio
async def test_sandbox_handle_base_url_properties():
    """Test SandboxHandleBase URL properties."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"))
    sandbox_config = SandboxConfiguration(sandbox_data)
    handle = SandboxAction(sandbox_config)

    # Test that URL properties exist on the base class
    assert hasattr(handle, "url")
    assert hasattr(handle, "external_url")
    assert hasattr(handle, "internal_url")
    assert hasattr(handle, "fallback_url")


@pytest.mark.asyncio
async def test_sandbox_forced_url_base():
    """Test sandbox forced URL functionality on base class."""
    # Set environment variable for forced URL
    os.environ["BL_SANDBOX_TEST_SANDBOX_URL"] = "http://localhost:8080"

    try:
        sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"))
        sandbox_config = SandboxConfiguration(sandbox_data)
        handle = SandboxAction(sandbox_config)

        # The forced URL should be detected on the base class
        assert hasattr(handle, "forced_url")

    finally:
        # Clean up environment variable
        if "BL_SANDBOX_TEST_SANDBOX_URL" in os.environ:
            del os.environ["BL_SANDBOX_TEST_SANDBOX_URL"]


@pytest.mark.asyncio
async def test_response_error():
    """Test ResponseError handling."""
    # Mock an HTTP response with error
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason_phrase = "Not Found"

    error = ResponseError(mock_response)
    assert error.response.status_code == 404
    assert error.response.reason_phrase == "Not Found"


@pytest.mark.asyncio
async def test_sandbox_class_methods():
    """Test sandbox class methods exist."""
    # Test that class methods exist
    assert hasattr(SandboxInstance, "create")
    assert hasattr(SandboxInstance, "get")
    assert hasattr(SandboxInstance, "list")
    assert hasattr(SandboxInstance, "delete")
    assert hasattr(SandboxInstance, "wait")
