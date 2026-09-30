"""Tests for sandbox functionality."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxLifecycle, SandboxSpec
from blaxel.core.sandbox import (
    CodeInterpreter,
    SandboxAPIError,
    SandboxInstance,
    SyncCodeInterpreter,
    SyncSandboxInstance,
)
from blaxel.core.sandbox.default.action import SandboxAction
from blaxel.core.sandbox.types import (
    ResponseError,
    SandboxConfiguration,
    SandboxUpdateMetadata,
    SandboxUpdateNetwork,
)


def sandbox_instance(name: str, status: str = "DEPLOYED", cls=SandboxInstance):
    sandbox_data = Sandbox(metadata=Metadata(name=name), spec=SandboxSpec())
    sandbox_data.status = status
    return cls(sandbox_data)


def conflict_error() -> SandboxAPIError:
    return SandboxAPIError("already exists", status_code=409)


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
async def test_create_if_not_exists_surfaces_conflict_without_retrying():
    with (
        patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create,
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
    ):
        mock_create.side_effect = conflict_error()

        with pytest.raises(SandboxAPIError) as raised:
            await SandboxInstance.create_if_not_exists({"name": "taken"})

        assert raised.value.status_code == 409
        mock_create.assert_awaited_once_with({"name": "taken"}, create_if_not_exist=True)
        mock_get.assert_not_called()


@pytest.mark.asyncio
async def test_create_if_not_exists_propagates_create_errors():
    with patch.object(SandboxInstance, "create", new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = SandboxAPIError("internal error", status_code=500)

        with pytest.raises(SandboxAPIError, match="internal error"):
            await SandboxInstance.create_if_not_exists({"name": "broken"})


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


def test_sync_create_if_not_exists_surfaces_conflict_without_retrying():
    with (
        patch.object(SyncSandboxInstance, "create") as mock_create,
        patch.object(SyncSandboxInstance, "get") as mock_get,
    ):
        mock_create.side_effect = conflict_error()

        with pytest.raises(SandboxAPIError) as raised:
            SyncSandboxInstance.create_if_not_exists({"name": "taken"})

        assert raised.value.status_code == 409
        mock_create.assert_called_once_with({"name": "taken"}, create_if_not_exist=True)
        mock_get.assert_not_called()


def test_sync_create_if_not_exists_propagates_create_errors():
    with patch.object(SyncSandboxInstance, "create") as mock_create:
        mock_create.side_effect = SandboxAPIError("internal error", status_code=500)

        with pytest.raises(SandboxAPIError, match="internal error"):
            SyncSandboxInstance.create_if_not_exists({"name": "broken"})


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


def _session_dict() -> dict:
    return {
        "name": "my-sandbox-session",
        "url": "https://preview.example.run.blaxel.ai/sandbox",
        "token": "super-secret-preview-token",
        "expires_at": "2999-01-01T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_from_session_does_not_leak_token_in_params():
    """The preview token must only travel in the header, never as a URL query param."""
    session = _session_dict()

    instance = await SandboxInstance.from_session(session)

    assert instance.config.params == {}
    assert instance.config.headers == {"X-Blaxel-Preview-Token": session["token"]}
    # The persistent HTTP client must not carry the token as a default query param.
    client = instance.process.get_client()
    assert session["token"] not in str(client.params)


def test_sync_from_session_does_not_leak_token_in_params():
    session = _session_dict()

    instance = SyncSandboxInstance.from_session(session)

    assert instance.config.params == {}
    assert instance.config.headers == {"X-Blaxel-Preview-Token": session["token"]}
    client = instance.process.get_client()
    assert session["token"] not in str(client.params)


def _body_metadata_name(body):
    """Read metadata.name from a create body that may be a Sandbox or a dict."""
    if isinstance(body, dict):
        return body["metadata"].get("name")
    return body.metadata.name


# ENG-3931: unnamed creations must reach the API without metadata.name so the
# server can assign one and the request is eligible for warm sandbox pools.


@pytest.mark.asyncio
async def test_create_omits_name_when_no_name_provided():
    created = sandbox_instance("srv-assigned").sandbox

    with patch(
        "blaxel.core.sandbox.default.sandbox.create_sandbox",
        new_callable=AsyncMock,
    ) as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        result = await SandboxInstance.create({"image": "custom:latest", "region": "us-pdx-1"})

        body = mock_create_sandbox.await_args.kwargs["body"]
        assert isinstance(body, dict)
        assert "name" not in body["metadata"]
        assert result.metadata.name == "srv-assigned"


@pytest.mark.asyncio
async def test_create_sends_name_when_provided():
    created = sandbox_instance("mysbx").sandbox

    with patch(
        "blaxel.core.sandbox.default.sandbox.create_sandbox",
        new_callable=AsyncMock,
    ) as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        await SandboxInstance.create({"name": "mysbx", "region": "us-pdx-1"})

        body = mock_create_sandbox.await_args.kwargs["body"]
        assert _body_metadata_name(body) == "mysbx"


@pytest.mark.asyncio
async def test_create_raw_model_without_name_omits_name():
    created = sandbox_instance("srv-assigned").sandbox

    with patch(
        "blaxel.core.sandbox.default.sandbox.create_sandbox",
        new_callable=AsyncMock,
    ) as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        await SandboxInstance.create(Sandbox(metadata=None, spec=SandboxSpec()))

        body = mock_create_sandbox.await_args.kwargs["body"]
        assert isinstance(body, dict)
        assert "name" not in body["metadata"]


def test_sync_create_omits_name_when_no_name_provided():
    created = sandbox_instance("srv-assigned", cls=SyncSandboxInstance).sandbox

    with patch("blaxel.core.sandbox.sync.sandbox.create_sandbox") as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        result = SyncSandboxInstance.create({"image": "custom:latest", "region": "us-pdx-1"})

        body = mock_create_sandbox.call_args.kwargs["body"]
        assert isinstance(body, dict)
        assert "name" not in body["metadata"]
        assert result.metadata.name == "srv-assigned"


def test_sync_create_sends_name_when_provided():
    created = sandbox_instance("mysbx", cls=SyncSandboxInstance).sandbox

    with patch("blaxel.core.sandbox.sync.sandbox.create_sandbox") as mock_create_sandbox:
        mock_create_sandbox.return_value = created

        SyncSandboxInstance.create({"name": "mysbx", "region": "us-pdx-1"})

        body = mock_create_sandbox.call_args.kwargs["body"]
        assert _body_metadata_name(body) == "mysbx"


@pytest.mark.asyncio
async def test_fork_defaults_to_sandbox_target():
    sandbox = sandbox_instance("my-sandbox")

    with patch(
        "blaxel.core.sandbox.default.sandbox.fork_sandbox", new_callable=AsyncMock
    ) as mock_fork:
        mock_fork.return_value = MagicMock(name="my-sandbox-copy", type="sandbox")

        await sandbox.fork("my-sandbox-copy")

        assert mock_fork.call_args.args[0] == "my-sandbox"
        body = mock_fork.call_args.kwargs["body"]
        assert body.target_name == "my-sandbox-copy"
        assert body.target_type == "sandbox"


@pytest.mark.asyncio
async def test_fork_forwards_application_options_and_snapshot():
    sandbox = sandbox_instance("my-sandbox")

    with patch(
        "blaxel.core.sandbox.default.sandbox.fork_sandbox", new_callable=AsyncMock
    ) as mock_fork:
        mock_fork.return_value = MagicMock()

        await sandbox.fork(
            "my-app",
            target_type="application",
            traffic=100,
            port=8080,
            custom_domain="app.example.com",
            snapshot_id="snap_abc123",
        )

        body = mock_fork.call_args.kwargs["body"]
        assert body.target_name == "my-app"
        assert body.target_type == "application"
        assert body.traffic == 100
        assert body.port == 8080
        assert body.custom_domain == "app.example.com"
        assert body.snapshot_id == "snap_abc123"


@pytest.mark.asyncio
async def test_fork_sends_lifecycle_only_when_given():
    sandbox = sandbox_instance("my-sandbox")
    lifecycle = {
        "expirationPolicies": [{"type": "ttl-max-age", "value": "45m", "action": "delete"}]
    }

    with patch(
        "blaxel.core.sandbox.default.sandbox.fork_sandbox", new_callable=AsyncMock
    ) as mock_fork:
        mock_fork.return_value = MagicMock()

        await sandbox.fork("inherited")
        assert "lifecycle" not in mock_fork.call_args.kwargs["body"].to_dict()

        await sandbox.fork("requested", lifecycle=SandboxLifecycle.from_dict(lifecycle))
        assert mock_fork.call_args.kwargs["body"].to_dict()["lifecycle"] == lifecycle

        await sandbox.fork("requested", lifecycle=lifecycle)
        assert mock_fork.call_args.kwargs["body"].to_dict()["lifecycle"] == lifecycle

        await sandbox.fork(
            "requested",
            lifecycle={"expiration_policies": lifecycle["expirationPolicies"]},
        )
        assert mock_fork.call_args.kwargs["body"].to_dict()["lifecycle"] == lifecycle


@pytest.mark.asyncio
async def test_snapshot_sends_optional_name():
    sandbox = sandbox_instance("my-sandbox")

    with patch(
        "blaxel.core.sandbox.default.sandbox.create_sandbox_snapshot", new_callable=AsyncMock
    ) as mock_snapshot:
        mock_snapshot.return_value = MagicMock()

        await sandbox.snapshot("before")

        assert mock_snapshot.call_args.args[0] == "my-sandbox"
        assert mock_snapshot.call_args.kwargs["body"].name == "before"


@pytest.mark.asyncio
async def test_delete_snapshot_accepts_none_204_response():
    sandbox = sandbox_instance("my-sandbox")

    with patch(
        "blaxel.core.sandbox.default.sandbox.delete_sandbox_snapshot", new_callable=AsyncMock
    ) as mock_delete:
        # Generated client returns None for a successful 204 No Content.
        mock_delete.return_value = None

        await sandbox.delete_snapshot("snap_abc123")

        assert mock_delete.call_args.args == ("my-sandbox", "snap_abc123")


@pytest.mark.asyncio
async def test_fork_raises_on_error_response():
    from blaxel.core.client.models.error import Error

    sandbox = sandbox_instance("my-sandbox")

    with patch(
        "blaxel.core.sandbox.default.sandbox.fork_sandbox", new_callable=AsyncMock
    ) as mock_fork:
        mock_fork.return_value = Error(error="boom", code=400)

        with pytest.raises(SandboxAPIError):
            await sandbox.fork("my-sandbox-copy")


def test_sync_fork_and_snapshot_helpers():
    sandbox = sandbox_instance("my-sandbox", cls=SyncSandboxInstance)

    with (
        patch("blaxel.core.sandbox.sync.sandbox.fork_sandbox") as mock_fork,
        patch("blaxel.core.sandbox.sync.sandbox.create_sandbox_snapshot") as mock_snapshot,
    ):
        mock_fork.return_value = MagicMock()
        mock_snapshot.return_value = MagicMock()

        sandbox.fork(
            "my-sandbox-copy",
            snapshot_id="snap_abc123",
            lifecycle={"expirationPolicies": [{"type": "ttl-idle", "value": "1h"}]},
        )
        sandbox.snapshot("before")

        fork_body = mock_fork.call_args.kwargs["body"]
        assert fork_body.target_name == "my-sandbox-copy"
        assert fork_body.target_type == "sandbox"
        assert fork_body.snapshot_id == "snap_abc123"
        assert fork_body.to_dict()["lifecycle"] == {
            "expirationPolicies": [{"type": "ttl-idle", "value": "1h"}]
        }
        assert mock_snapshot.call_args.kwargs["body"].name == "before"


# --- Control-plane errors must not be returned as if they were sandboxes -------
#
# Every generated API function returns ``Union[Error, Sandbox] | None``. The
# update_*/delete helpers used to hand that straight to ``cls(...)``, so a 403 or
# 500 produced an instance wrapping an ``Error``: a failed write looked like a
# success to any caller that did not inspect the return value, and callers that
# did inspect it hit ``AttributeError`` far away from the real cause.


def api_error(code=403, message="insufficient permissions"):
    from blaxel.core.client.models.error import Error

    return Error(error="FORBIDDEN", code=code, message=message)


def updatable_sandbox(name="my-sandbox", cls=SandboxInstance):
    """An instance the update_* helpers can round-trip through ``to_dict()``.

    ``sandbox_instance`` assigns ``status`` as a plain string, which the generated
    model cannot serialize; the update helpers re-serialize the fetched sandbox.
    """
    return cls(Sandbox(metadata=Metadata(name=name), spec=SandboxSpec()))


UPDATE_CALLS = [
    ("update_metadata", lambda: SandboxUpdateMetadata(labels={"team": "core"})),
    ("update_ttl", lambda: "10m"),
    ("update_lifecycle", lambda: None),
    ("update_network", lambda: SandboxUpdateNetwork(network=None)),
]


@pytest.mark.parametrize("method_name,arg_factory", UPDATE_CALLS)
@pytest.mark.asyncio
async def test_update_helpers_raise_on_error_response(method_name, arg_factory):
    with (
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
        patch(
            "blaxel.core.sandbox.default.sandbox.update_sandbox", new_callable=AsyncMock
        ) as mock_update,
    ):
        mock_get.return_value = updatable_sandbox()
        mock_update.return_value = api_error()

        with pytest.raises(SandboxAPIError, match="insufficient permissions") as excinfo:
            await getattr(SandboxInstance, method_name)("my-sandbox", arg_factory())

    assert excinfo.value.status_code == 403


@pytest.mark.parametrize("method_name,arg_factory", UPDATE_CALLS)
@pytest.mark.asyncio
async def test_update_helpers_raise_on_empty_response(method_name, arg_factory):
    with (
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
        patch(
            "blaxel.core.sandbox.default.sandbox.update_sandbox", new_callable=AsyncMock
        ) as mock_update,
    ):
        mock_get.return_value = updatable_sandbox()
        mock_update.return_value = None

        with pytest.raises(SandboxAPIError):
            await getattr(SandboxInstance, method_name)("my-sandbox", arg_factory())


@pytest.mark.asyncio
async def test_update_helpers_still_return_instance_on_success():
    with (
        patch.object(SandboxInstance, "get", new_callable=AsyncMock) as mock_get,
        patch(
            "blaxel.core.sandbox.default.sandbox.update_sandbox", new_callable=AsyncMock
        ) as mock_update,
    ):
        mock_get.return_value = updatable_sandbox()
        mock_update.return_value = Sandbox(metadata=Metadata(name="my-sandbox"), spec=SandboxSpec())

        result = await SandboxInstance.update_ttl("my-sandbox", "10m")

        assert isinstance(result, SandboxInstance)
        assert result.metadata.name == "my-sandbox"


@pytest.mark.asyncio
async def test_delete_raises_on_error_response():
    with patch(
        "blaxel.core.sandbox.default.sandbox.delete_sandbox", new_callable=AsyncMock
    ) as mock_delete:
        mock_delete.return_value = api_error(code=500, message="control plane exploded")

        with pytest.raises(SandboxAPIError, match="control plane exploded"):
            await SandboxInstance.delete("my-sandbox")


@pytest.mark.asyncio
async def test_delete_raises_on_empty_response():
    with patch(
        "blaxel.core.sandbox.default.sandbox.delete_sandbox", new_callable=AsyncMock
    ) as mock_delete:
        mock_delete.return_value = None

        with pytest.raises(SandboxAPIError, match="delete sandbox my-sandbox"):
            await SandboxInstance.delete("my-sandbox")


@pytest.mark.asyncio
async def test_instance_delete_raises_on_error_response():
    sandbox = sandbox_instance("my-sandbox")

    with patch(
        "blaxel.core.sandbox.default.sandbox.delete_sandbox", new_callable=AsyncMock
    ) as mock_delete:
        mock_delete.return_value = api_error(code=404, message="sandbox not found")

        with pytest.raises(SandboxAPIError, match="sandbox not found"):
            await sandbox.delete()


@pytest.mark.parametrize("method_name,arg_factory", UPDATE_CALLS)
def test_sync_update_helpers_raise_on_error_response(method_name, arg_factory):
    with (
        patch.object(SyncSandboxInstance, "get") as mock_get,
        patch("blaxel.core.sandbox.sync.sandbox.update_sandbox") as mock_update,
    ):
        mock_get.return_value = updatable_sandbox(cls=SyncSandboxInstance)
        mock_update.return_value = api_error()

        with pytest.raises(SandboxAPIError, match="insufficient permissions"):
            getattr(SyncSandboxInstance, method_name)("my-sandbox", arg_factory())


def test_sync_delete_raises_on_error_response():
    with patch("blaxel.core.sandbox.sync.sandbox.delete_sandbox") as mock_delete:
        mock_delete.return_value = api_error(code=500, message="control plane exploded")

        with pytest.raises(SandboxAPIError, match="control plane exploded"):
            SyncSandboxInstance.delete("my-sandbox")
