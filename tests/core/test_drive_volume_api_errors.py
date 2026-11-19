"""Drive and volume wrappers raise their typed error, carrying the API's message.

The generated client returns an ``Error`` for the statuses an operation declares
and raises ``UnexpectedStatus`` (or a subclass such as ``ConflictError``) for the
others. Callers should not have to know which: every error status reaches them
as ``DriveAPIError`` or ``VolumeAPIError``, never as ``None`` or an untyped error.
The responses below are built against the real generated client, through httpx.
"""

import json
from unittest.mock import AsyncMock

import httpx
import pytest

from blaxel.core.client.client import client as api_client
from blaxel.core.client.errors import UnexpectedStatus
from blaxel.core.client.models import DeleteDriveResponse200
from blaxel.core.drive import drive as drive_module
from blaxel.core.drive.drive import DriveAPIError, DriveInstance, SyncDriveInstance
from blaxel.core.errors import BlaxelError
from blaxel.core.volume import volume as volume_module
from blaxel.core.volume.volume import SyncVolumeInstance, VolumeAPIError, VolumeInstance

DRIVE = {"metadata": {"name": "data"}, "spec": {"region": "us-pdx-1"}, "status": "DEPLOYED"}
VOLUME = {
    "metadata": {"name": "data"},
    "spec": {"size": 2048, "region": "us-pdx-1", "template": "base"},
    "status": "DEPLOYED",
}

# What the control plane answers for each status, as {error, code}.
DRIVE_MESSAGES = {
    400: "Invalid drive name",
    401: "Unauthorized",
    403: "Drives feature is not enabled for this workspace",
    404: "Drive not found",
    409: "Drive already exists",
}

# A registered error: the v0 body keeps error (message) and code (status) and
# adds the platform fields next to them.
AUTHENTICATION_REQUIRED = {
    "error": "Unauthorized",
    "code": 401,
    "error_code": "AUTHENTICATION_REQUIRED",
    "message": "Unauthorized",
    "action": "Send a credential with the request, then resend it.",
    "do_not": "Do not retry without a credential.",
    "docs_url": "https://docs.blaxel.ai/errors#AUTHENTICATION_REQUIRED",
    "retryable": False,
    "safe_to_retry_request": True,
    "dispatch_state": "not_dispatched",
    "status": 401,
    "origin": "platform",
    "timestamp": "2026-11-18T12:00:00Z",
    "request_id": "req-123",
}


def error_body(status: int, message: str) -> dict:
    return {"error": message, "code": status}


@pytest.fixture
def serve(monkeypatch):
    """Answer the SDK's requests with ``handler(request) -> (status, json)``."""
    monkeypatch.setattr(drive_module.asyncio, "sleep", AsyncMock())
    monkeypatch.setattr(volume_module.asyncio, "sleep", AsyncMock())
    monkeypatch.setattr(drive_module.time, "sleep", lambda _: None, raising=False)
    monkeypatch.setattr(volume_module.time, "sleep", lambda _: None, raising=False)
    requests: list[httpx.Request] = []

    def install(handler):
        def respond(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            status, body = handler(request)
            return httpx.Response(status, json=body, request=request)

        transport = httpx.MockTransport(respond)
        sync_http = httpx.Client(base_url="https://api.blaxel.test", transport=transport)
        async_http = httpx.AsyncClient(base_url="https://api.blaxel.test", transport=transport)
        monkeypatch.setattr(type(api_client), "get_httpx_client", lambda self: sync_http)
        monkeypatch.setattr(type(api_client), "get_async_httpx_client", lambda self: async_http)
        return requests

    return install


def drive_failing(method: str, status: int):
    """Fail ``method`` with ``status``; a GET before it (update reads first) succeeds."""

    def handler(request):
        if request.method == method:
            return status, error_body(status, DRIVE_MESSAGES[status])
        return 200, DRIVE

    return handler


async def call_async(operation: str):
    if operation == "create":
        return await DriveInstance.create({"name": "data", "region": "us-pdx-1"})
    if operation == "get":
        return await DriveInstance.get("data")
    if operation == "update":
        return await DriveInstance.update("data", {"labels": {"team": "a"}})
    return await DriveInstance.delete("data")


def call_sync(operation: str):
    if operation == "create":
        return SyncDriveInstance.create({"name": "data", "region": "us-pdx-1"})
    if operation == "get":
        return SyncDriveInstance.get("data")
    if operation == "update":
        return SyncDriveInstance.update("data", {"labels": {"team": "a"}})
    return SyncDriveInstance.delete("data")


METHODS = {"create": "POST", "get": "GET", "update": "PUT", "delete": "DELETE"}
DRIVE_CASES = [(operation, status) for operation in METHODS for status in DRIVE_MESSAGES]


def assert_drive_error(error: DriveAPIError, status: int) -> None:
    assert type(error) is DriveAPIError
    assert error.status_code == status
    assert error.status == status
    assert error.message == DRIVE_MESSAGES[status]
    assert DRIVE_MESSAGES[status] in str(error)


@pytest.mark.asyncio
@pytest.mark.parametrize(("operation", "status"), DRIVE_CASES)
async def test_async_drive_errors_raise_drive_api_error(serve, operation, status):
    serve(drive_failing(METHODS[operation], status))

    with pytest.raises(DriveAPIError) as error:
        await call_async(operation)

    assert_drive_error(error.value, status)


@pytest.mark.parametrize(("operation", "status"), DRIVE_CASES)
def test_sync_drive_errors_raise_drive_api_error(serve, operation, status):
    serve(drive_failing(METHODS[operation], status))

    with pytest.raises(DriveAPIError) as error:
        call_sync(operation)

    assert_drive_error(error.value, status)


@pytest.mark.asyncio
async def test_drive_status_the_client_does_not_declare_keeps_its_cause(serve):
    # create declares 409 nowhere, so the generated client raises ConflictError.
    serve(drive_failing("POST", 409))

    with pytest.raises(DriveAPIError) as error:
        await DriveInstance.create({"name": "data", "region": "us-pdx-1"})

    assert isinstance(error.value.__cause__, UnexpectedStatus)
    assert error.value.code == DRIVE_MESSAGES[409]


@pytest.mark.asyncio
async def test_async_get_drive_with_a_bad_api_key_reports_401(serve):
    serve(lambda request: (401, AUTHENTICATION_REQUIRED))

    with pytest.raises(DriveAPIError) as error:
        await DriveInstance.get("data")

    assert error.value.status_code == 401


def test_sync_get_drive_with_a_bad_api_key_reports_401(serve):
    serve(lambda request: (401, AUTHENTICATION_REQUIRED))

    with pytest.raises(DriveAPIError) as error:
        SyncDriveInstance.get("data")

    assert error.value.status_code == 401


@pytest.mark.asyncio
async def test_async_drive_delete_returns_its_response_model(serve):
    serve(lambda request: (200, {"message": "Drive deletion started", "name": "data"}))

    result = await DriveInstance.delete("data")

    assert isinstance(result, DeleteDriveResponse200)
    assert result.name == "data"


def test_sync_drive_delete_returns_its_response_model(serve):
    serve(lambda request: (200, {"message": "Drive deletion started", "name": "data"}))

    result = SyncDriveInstance.delete("data")

    assert isinstance(result, DeleteDriveResponse200)
    assert result.message == "Drive deletion started"


def volume_server(request):
    """Answer like the control plane: reads succeed, updates go through its rules."""
    if request.method == "GET":
        return 200, VOLUME
    if request.method == "DELETE":
        return 400, error_body(400, "Volume is attached to sandbox my-sandbox")
    spec = json.loads(request.content)["spec"]
    current = VOLUME["spec"]
    if spec.get("size") and spec["size"] < current["size"]:
        message = (
            "volume size cannot be decreased. New size must be greater than or equal "
            "to the current size (2048 MB)"
        )
        return 400, error_body(400, message)
    if spec.get("region") and spec["region"] != current["region"]:
        return 400, error_body(400, "volume region cannot be changed after creation")
    if spec.get("template") and spec["template"] != current["template"]:
        return 400, error_body(400, "volume template cannot be changed after creation")
    return 200, VOLUME


VOLUME_UPDATES = [
    ({"size": 1024}, "volume size cannot be decreased"),
    ({"region": "eu-lon-1"}, "volume region cannot be changed after creation"),
    ({"template": "other"}, "volume template cannot be changed after creation"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("updates", "message"), VOLUME_UPDATES)
async def test_async_rejected_volume_update_raises_volume_api_error(serve, updates, message):
    serve(volume_server)

    with pytest.raises(VolumeAPIError, match=message) as error:
        await VolumeInstance.update("data", updates)

    assert error.value.status_code == 400


@pytest.mark.parametrize(("updates", "message"), VOLUME_UPDATES)
def test_sync_rejected_volume_update_raises_volume_api_error(serve, updates, message):
    serve(volume_server)

    with pytest.raises(VolumeAPIError, match=message) as error:
        SyncVolumeInstance.update("data", updates)

    assert error.value.status_code == 400


@pytest.mark.asyncio
async def test_async_deleting_an_attached_volume_raises_volume_api_error(serve):
    serve(volume_server)

    with pytest.raises(VolumeAPIError, match="Volume is attached to sandbox my-sandbox") as error:
        await VolumeInstance.delete("data")

    assert error.value.status_code == 400
    assert isinstance(error.value.__cause__, UnexpectedStatus)


def test_sync_deleting_an_attached_volume_raises_volume_api_error(serve):
    serve(volume_server)

    with pytest.raises(VolumeAPIError, match="Volume is attached to sandbox my-sandbox") as error:
        SyncVolumeInstance.delete("data")

    assert error.value.status_code == 400


def assert_contract_fields(error: BlaxelError) -> None:
    assert error.error_code == "AUTHENTICATION_REQUIRED"
    assert error.message == "Unauthorized"
    assert error.action == AUTHENTICATION_REQUIRED["action"]
    assert error.do_not == AUTHENTICATION_REQUIRED["do_not"]
    assert error.docs_url == AUTHENTICATION_REQUIRED["docs_url"]
    assert error.retryable is False
    assert error.safe_to_retry_request is True
    assert error.dispatch_state == "not_dispatched"
    assert error.request_id == "req-123"
    assert error.origin == "platform"


@pytest.mark.asyncio
async def test_drive_error_carries_the_error_contract_fields(serve):
    # get declares 401, so this goes through the generated Error model.
    serve(lambda request: (401, AUTHENTICATION_REQUIRED))

    with pytest.raises(DriveAPIError) as error:
        await DriveInstance.get("data")

    assert_contract_fields(error.value)
    # The legacy attributes keep their meaning.
    assert error.value.status_code == 401
    assert error.value.code == "Unauthorized"


@pytest.mark.asyncio
async def test_volume_error_from_an_undeclared_status_carries_the_contract_fields(serve):
    # delete does not declare 400, so this goes through UnexpectedStatus.
    body = {**AUTHENTICATION_REQUIRED, "code": 400, "status": 400}
    serve(lambda request: (400, body))

    with pytest.raises(VolumeAPIError) as error:
        await VolumeInstance.delete("data")

    assert_contract_fields(error.value)
    assert error.value.status_code == 400
    assert error.value.code == "Unauthorized"
