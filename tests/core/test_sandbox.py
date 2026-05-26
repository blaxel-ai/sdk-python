"""Tests for sandbox functionality."""

import os
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import (
    CodeInterpreter,
    SandboxAPIError,
    SandboxInstance,
    SyncCodeInterpreter,
    SyncSandboxInstance,
)
from blaxel.core.sandbox.default.action import SandboxAction
from blaxel.core.sandbox.types import ResponseError, SandboxConfiguration


def sandbox_instance(name: str, status: str = "DEPLOYED", cls=SandboxInstance):
    sandbox_data = Sandbox(metadata=Metadata(name=name), spec=SandboxSpec())
    sandbox_data.status = status
    return cls(sandbox_data)


def conflict_error() -> SandboxAPIError:
    return SandboxAPIError("already exists", status_code=409)


def conflict_error_with_code(code) -> SandboxAPIError:
    error = SandboxAPIError("already exists", code=code)
    error.code = code
    return error


@pytest.mark.asyncio
async def test_sandbox_creation():
    """Test sandbox instance creation."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"), spec=SandboxSpec())
    sandbox = SandboxInstance(sandbox_data)
    assert sandbox.sandbox.metadata.name == "test-sandbox"


@pytest.mark.asyncio
async def test_sandbox_properties():
    """Test sandbox instance properties."""
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"), spec=SandboxSpec())
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
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"), spec=SandboxSpec())
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
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"), spec=SandboxSpec())
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
    sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"), spec=SandboxSpec())
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
        sandbox_data = Sandbox(metadata=Metadata(name="test-sandbox"), spec=SandboxSpec())
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


@pytest.mark.asyncio
async def test_create_if_not_exists_uses_server_side_param():
    existing = sandbox_instance("existing")

    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.return_value = existing

        result = await SandboxInstance.create_if_not_exists({"name": "existing"})

        assert result is existing
        mock_create.assert_awaited_once_with({"name": "existing"}, create_if_not_exist=True)
        mock_get.assert_not_called()


@pytest.mark.asyncio
async def test_create_forwards_create_if_not_exist_to_generated_client():
    created = sandbox_instance("created").sandbox

    with patch(
        "blaxel.core.sandbox.default.sandbox.create_sandbox",
        new_callable=AsyncMock,
    ) as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        result = await SandboxInstance.create(
            {"name": "created", "region": "us-pdx-1"},
            create_if_not_exist=True,
        )

        assert result.metadata.name == "created"
        assert mock_create_sandbox.await_args.kwargs["create_if_not_exist"] is True


@pytest.mark.asyncio
async def test_create_if_not_exists_returns_existing_after_conflict():
    existing = sandbox_instance("existing")

    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.side_effect = [conflict_error()]
        mock_get.return_value = existing

        result = await SandboxInstance.create_if_not_exists({"name": "existing"})

        assert result is existing
        mock_create.assert_awaited_once_with({"name": "existing"}, create_if_not_exist=True)
        mock_get.assert_awaited_once_with("existing")


@pytest.mark.asyncio
@pytest.mark.parametrize("code", ["SANDBOX_ALREADY_EXISTS", "409", 409])
async def test_create_if_not_exists_accepts_conflict_error_codes(code):
    existing = sandbox_instance("existing")

    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.side_effect = [conflict_error_with_code(code)]
        mock_get.return_value = existing

        result = await SandboxInstance.create_if_not_exists({"name": "existing"})

        assert result is existing
        mock_get.assert_awaited_once_with("existing")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status",
    ["FAILED", "TERMINATED", "TERMINATING", "DELETING", "DEACTIVATING"],
)
async def test_create_if_not_exists_retries_for_non_reusable_statuses(status):
    replacement = sandbox_instance("stale")

    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.side_effect = [conflict_error(), replacement]
        mock_get.return_value = sandbox_instance("stale", status)

        result = await SandboxInstance.create_if_not_exists({"name": "stale"})

        assert result is replacement
        assert mock_create.await_args_list == [
            call({"name": "stale"}, create_if_not_exist=True),
            call({"name": "stale"}, create_if_not_exist=True),
        ]


@pytest.mark.asyncio
async def test_create_if_not_exists_handles_recreate_race_after_terminal_status():
    winner = sandbox_instance("race")

    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.side_effect = [conflict_error(), conflict_error()]
        mock_get.side_effect = [sandbox_instance("race", "TERMINATED"), winner]

        result = await SandboxInstance.create_if_not_exists({"name": "race"})

        assert result is winner
        assert mock_create.await_count == 2
        assert mock_get.await_args_list == [call("race"), call("race")]


@pytest.mark.asyncio
async def test_create_if_not_exists_stops_after_bounded_attempts():
    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.side_effect = conflict_error()
        mock_get.return_value = sandbox_instance("stuck", "TERMINATED")

        with pytest.raises(RuntimeError, match="Unable to create sandbox after 3 attempts"):
            await SandboxInstance.create_if_not_exists({"name": "stuck"})

        assert mock_create.await_count == 3
        assert mock_get.await_count == 3


@pytest.mark.asyncio
async def test_code_interpreter_create_forwards_create_if_not_exist():
    with patch(
        "blaxel.core.sandbox.default.interpreter.SandboxInstance.create",
        new_callable=AsyncMock,
    ) as mock_create:
        mock_create.return_value = sandbox_instance("interpreter")

        result = await CodeInterpreter.create(
            {"name": "interpreter"},
            safe=False,
            create_if_not_exist=True,
        )

        assert isinstance(result, CodeInterpreter)
        payload = mock_create.await_args.args[0]
        assert payload["name"] == "interpreter"
        assert mock_create.await_args.kwargs == {
            "safe": False,
            "create_if_not_exist": True,
        }


@pytest.mark.asyncio
async def test_code_interpreter_create_if_not_exists_uses_server_side_param():
    with patch(
        "blaxel.core.sandbox.default.interpreter.SandboxInstance.create",
        new_callable=AsyncMock,
    ) as mock_create:
        mock_create.return_value = sandbox_instance("interpreter-existing")

        result = await CodeInterpreter.create_if_not_exists({"name": "interpreter-existing"})

        assert isinstance(result, CodeInterpreter)
        payload = mock_create.await_args.args[0]
        assert payload["name"] == "interpreter-existing"
        assert mock_create.await_args.kwargs == {
            "safe": True,
            "create_if_not_exist": True,
        }


def test_sync_create_if_not_exists_uses_server_side_param():
    existing = sandbox_instance("existing", cls=SyncSandboxInstance)

    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.return_value = existing

        result = SyncSandboxInstance.create_if_not_exists({"name": "existing"})

        assert result is existing
        mock_create.assert_called_once_with({"name": "existing"}, create_if_not_exist=True)
        mock_get.assert_not_called()


def test_sync_create_forwards_create_if_not_exist_to_generated_client():
    created = sandbox_instance("created", cls=SyncSandboxInstance).sandbox

    with patch("blaxel.core.sandbox.sync.sandbox.create_sandbox") as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        result = SyncSandboxInstance.create(
            {"name": "created", "region": "us-pdx-1"},
            create_if_not_exist=True,
        )

        assert result.metadata.name == "created"
        assert mock_create_sandbox.call_args.kwargs["create_if_not_exist"] is True


def test_sync_create_if_not_exists_returns_existing_after_conflict():
    existing = sandbox_instance("existing", cls=SyncSandboxInstance)

    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.side_effect = [conflict_error()]
        mock_get.return_value = existing

        result = SyncSandboxInstance.create_if_not_exists({"name": "existing"})

        assert result is existing
        mock_create.assert_called_once_with({"name": "existing"}, create_if_not_exist=True)
        mock_get.assert_called_once_with("existing")


@pytest.mark.parametrize("code", ["SANDBOX_ALREADY_EXISTS", "409", 409])
def test_sync_create_if_not_exists_accepts_conflict_error_codes(code):
    existing = sandbox_instance("existing", cls=SyncSandboxInstance)

    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.side_effect = [conflict_error_with_code(code)]
        mock_get.return_value = existing

        result = SyncSandboxInstance.create_if_not_exists({"name": "existing"})

        assert result is existing
        mock_get.assert_called_once_with("existing")


@pytest.mark.parametrize(
    "status",
    ["FAILED", "TERMINATED", "TERMINATING", "DELETING", "DEACTIVATING"],
)
def test_sync_create_if_not_exists_retries_for_non_reusable_statuses(status):
    replacement = sandbox_instance("stale", cls=SyncSandboxInstance)

    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.side_effect = [conflict_error(), replacement]
        mock_get.return_value = sandbox_instance("stale", status, cls=SyncSandboxInstance)

        result = SyncSandboxInstance.create_if_not_exists({"name": "stale"})

        assert result is replacement
        assert mock_create.call_args_list == [
            call({"name": "stale"}, create_if_not_exist=True),
            call({"name": "stale"}, create_if_not_exist=True),
        ]


def test_sync_create_if_not_exists_handles_recreate_race_after_terminal_status():
    winner = sandbox_instance("race", cls=SyncSandboxInstance)

    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.side_effect = [conflict_error(), conflict_error()]
        mock_get.side_effect = [
            sandbox_instance("race", "TERMINATED", cls=SyncSandboxInstance),
            winner,
        ]

        result = SyncSandboxInstance.create_if_not_exists({"name": "race"})

        assert result is winner
        assert mock_create.call_count == 2
        assert mock_get.call_args_list == [call("race"), call("race")]


def test_sync_create_if_not_exists_stops_after_bounded_attempts():
    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.side_effect = conflict_error()
        mock_get.return_value = sandbox_instance("stuck", "TERMINATED", cls=SyncSandboxInstance)

        with pytest.raises(RuntimeError, match="Unable to create sandbox after 3 attempts"):
            SyncSandboxInstance.create_if_not_exists({"name": "stuck"})

        assert mock_create.call_count == 3
        assert mock_get.call_count == 3


def test_sync_code_interpreter_create_forwards_create_if_not_exist():
    with patch("blaxel.core.sandbox.sync.interpreter.SyncSandboxInstance.create") as mock_create:
        mock_create.return_value = sandbox_instance("interpreter", cls=SyncSandboxInstance)

        result = SyncCodeInterpreter.create(
            {"name": "interpreter"},
            safe=False,
            create_if_not_exist=True,
        )

        assert isinstance(result, SyncCodeInterpreter)
        payload = mock_create.call_args.args[0]
        assert payload["name"] == "interpreter"
        assert mock_create.call_args.kwargs == {
            "safe": False,
            "create_if_not_exist": True,
        }


def test_sync_code_interpreter_create_if_not_exists_uses_server_side_param():
    with patch("blaxel.core.sandbox.sync.interpreter.SyncSandboxInstance.create") as mock_create:
        mock_create.return_value = sandbox_instance("interpreter-existing", cls=SyncSandboxInstance)

        result = SyncCodeInterpreter.create_if_not_exists({"name": "interpreter-existing"})

        assert isinstance(result, SyncCodeInterpreter)
        payload = mock_create.call_args.args[0]
        assert payload["name"] == "interpreter-existing"
        assert mock_create.call_args.kwargs == {
            "safe": True,
            "create_if_not_exist": True,
        }
