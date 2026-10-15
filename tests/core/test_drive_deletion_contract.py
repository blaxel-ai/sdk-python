"""Exercise the deletion integration assertion against real generated HTTP parsing."""

import asyncio
from unittest.mock import AsyncMock

import httpx
import pytest

from blaxel.core.client.errors import UnexpectedStatus
from tests.integration.core.sandbox import test_drives as drive_tests


@pytest.mark.asyncio
@pytest.mark.parametrize("statuses", [(200, 200, 404), (404,), (401,), (502,)])
async def test_drive_deletion_requires_http_not_found(monkeypatch, statuses):
    observed = []

    def respond(request):
        status = statuses[len(observed)]
        observed.append(status)
        return httpx.Response(
            status, json={"metadata": {"name": "deleting-drive"}, "spec": {}, "status": "DELETING"}
        )

    drive = AsyncMock()
    monkeypatch.setattr(drive_tests.DriveInstance, "create", AsyncMock(return_value=drive))
    monkeypatch.setattr(drive_tests.asyncio, "sleep", AsyncMock())
    case = drive_tests.TestDriveInstanceCRUD()
    case.created_drives = []
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(respond), base_url="https://test"
    ) as http:
        monkeypatch.setattr(type(drive_tests.client), "get_async_httpx_client", lambda self: http)
        if statuses[-1] == 404:
            await case.test_deletes_a_drive()
        elif statuses[-1] == 401:
            with pytest.raises(AssertionError, match="401"):
                await case.test_deletes_a_drive()
        else:
            with pytest.raises(UnexpectedStatus) as error:
                await case.test_deletes_a_drive()
            assert error.value.status_code == 502
    assert observed == list(statuses)
    drive.delete.assert_awaited_once()
    assert len(case.created_drives) == 1


@pytest.mark.asyncio
async def test_drive_deletion_has_bounded_wait(monkeypatch):
    drive = AsyncMock()
    monkeypatch.setattr(drive_tests.DriveInstance, "create", AsyncMock(return_value=drive))
    original_wait_for = asyncio.wait_for

    async def short_deadline(awaitable, timeout):
        assert timeout == 45
        return await original_wait_for(awaitable, timeout=0.01)

    monkeypatch.setattr(drive_tests.asyncio, "wait_for", short_deadline)
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})),
        base_url="https://test",
    ) as http:
        monkeypatch.setattr(type(drive_tests.client), "get_async_httpx_client", lambda self: http)
        with pytest.raises(asyncio.TimeoutError):
            await drive_tests.TestDriveInstanceCRUD().test_deletes_a_drive()
