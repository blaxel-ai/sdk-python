"""Unit tests for the per-request creation timeout on SandboxInstance.create.

The control plane reads ``X-Blaxel-Creation-Timeout`` (whole seconds) and answers
``408`` / ``CREATION_TIMEOUT`` when the sandbox is not ready in time. The SDK
forwards the header only when asked, caps it at 50s, and surfaces that failure as
a dedicated ``SandboxCreationTimeoutError`` so callers can catch it precisely.
"""

import json
from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core import (
    SandboxAPIError,
    SandboxCreationTimeoutError,
    SandboxInstance,
    SyncSandboxInstance,
    is_creation_timeout_error,
)
from blaxel.core.client import errors as client_errors
from blaxel.core.client.client import client as shared_client
from blaxel.core.client.models import Metadata, Sandbox, SandboxRuntime, SandboxSpec
from blaxel.core.client.models.sandbox_error import SandboxError
from blaxel.core.sandbox import MAX_CREATION_TIMEOUT_SECONDS
from blaxel.core.sandbox.default.sandbox import CREATION_TIMEOUT_HEADER

ASYNC_CREATE = "blaxel.core.sandbox.default.sandbox.create_sandbox"
SYNC_CREATE = "blaxel.core.sandbox.sync.sandbox.create_sandbox"
CONFIG = {"name": "timed", "region": "us-pdx-1"}


def _created(name: str = "timed") -> Sandbox:
    return Sandbox(
        metadata=Metadata(name=name),
        spec=SandboxSpec(runtime=SandboxRuntime(image="blaxel/base-image:latest")),
    )


def _timeout_408() -> client_errors.UnexpectedStatus:
    body = {"code": "CREATION_TIMEOUT", "message": "sandbox not ready in time"}
    return client_errors.UnexpectedStatus(408, json.dumps(body).encode())


@pytest.mark.asyncio
async def test_no_timeout_uses_shared_client_without_header():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created()

        await SandboxInstance.create(CONFIG)

        used = mock_create.await_args.kwargs["client"]
        assert used is shared_client
        assert CREATION_TIMEOUT_HEADER not in used._headers


@pytest.mark.asyncio
async def test_timeout_is_sent_as_header_without_touching_shared_client():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created()

        await SandboxInstance.create(CONFIG, timeout=30)

        used = mock_create.await_args.kwargs["client"]
        assert used is not shared_client
        assert used._headers[CREATION_TIMEOUT_HEADER] == "30"
        assert CREATION_TIMEOUT_HEADER not in shared_client._headers
        # Everything else about the shared client is preserved on the copy.
        assert used._base_url == shared_client._base_url


@pytest.mark.parametrize("timeout", [0, -1, 51, MAX_CREATION_TIMEOUT_SECONDS + 1, 1.5, True, "10"])
@pytest.mark.asyncio
async def test_rejects_out_of_range_or_non_integer_timeout(timeout):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        with pytest.raises(ValueError, match="between 1 and 50"):
            await SandboxInstance.create(CONFIG, timeout=timeout)
        mock_create.assert_not_awaited()


@pytest.mark.parametrize("timeout", [1, MAX_CREATION_TIMEOUT_SECONDS])
@pytest.mark.asyncio
async def test_accepts_timeout_bounds(timeout):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created()
        await SandboxInstance.create(CONFIG, timeout=timeout)
        assert mock_create.await_args.kwargs["client"]._headers[CREATION_TIMEOUT_HEADER] == str(
            timeout
        )


@pytest.mark.asyncio
async def test_408_becomes_creation_timeout_error():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = _timeout_408()

        with pytest.raises(SandboxCreationTimeoutError) as excinfo:
            await SandboxInstance.create(CONFIG, timeout=20)

    err = excinfo.value
    assert is_creation_timeout_error(err)
    assert isinstance(err, SandboxAPIError)
    assert err.code == "CREATION_TIMEOUT"
    assert err.status_code == 408
    assert err.sandbox_name == "timed"
    assert err.timeout == 20
    assert err.data["message"] == "sandbox not ready in time"
    assert "timed" in str(err) and "20s" in str(err) and "sandbox not ready in time" in str(err)


@pytest.mark.asyncio
async def test_structured_creation_timeout_error_becomes_creation_timeout_error():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = SandboxError(
            code="CREATION_TIMEOUT", message="took too long", status_code=408
        )

        with pytest.raises(SandboxCreationTimeoutError) as excinfo:
            await SandboxInstance.create(CONFIG)

    assert excinfo.value.timeout is None
    assert excinfo.value.sandbox_name == "timed"
    assert "creation deadline" in str(excinfo.value)


@pytest.mark.asyncio
async def test_other_errors_are_left_unchanged():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = SandboxError(code="QUOTA", message="nope", status_code=403)
        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG, timeout=10)
        assert not is_creation_timeout_error(excinfo.value)
        assert excinfo.value.status_code == 403

    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = client_errors.UnexpectedStatus(502, b"bad gateway")
        with pytest.raises(client_errors.UnexpectedStatus):
            await SandboxInstance.create(CONFIG, timeout=10)


@pytest.mark.asyncio
async def test_caller_can_catch_the_timeout_and_recover():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_timeout_408(), _created()]

        try:
            await SandboxInstance.create(CONFIG, timeout=5)
        except SandboxCreationTimeoutError:
            result = await SandboxInstance.create(CONFIG, timeout=5)

        assert result.metadata.name == "timed"
        assert mock_create.await_count == 2


@pytest.mark.asyncio
async def test_create_if_not_exists_forwards_timeout():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created()

        await SandboxInstance.create_if_not_exists(CONFIG, timeout=15)

        kwargs = mock_create.await_args.kwargs
        assert kwargs["create_if_not_exist"] is True
        assert kwargs["client"]._headers[CREATION_TIMEOUT_HEADER] == "15"

    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = _timeout_408()
        with pytest.raises(SandboxCreationTimeoutError):
            await SandboxInstance.create_if_not_exists(CONFIG, timeout=15)
        mock_create.assert_awaited_once()


def test_sync_timeout_header_and_error():
    with patch(SYNC_CREATE) as mock_create:
        mock_create.return_value = _created()
        SyncSandboxInstance.create(CONFIG, timeout=25)
        assert mock_create.call_args.kwargs["client"]._headers[CREATION_TIMEOUT_HEADER] == "25"
        assert CREATION_TIMEOUT_HEADER not in shared_client._headers

    with patch(SYNC_CREATE) as mock_create:
        mock_create.side_effect = _timeout_408()
        with pytest.raises(SandboxCreationTimeoutError) as excinfo:
            SyncSandboxInstance.create_if_not_exists(CONFIG, timeout=25)
        assert excinfo.value.timeout == 25
        assert excinfo.value.sandbox_name == "timed"

    with pytest.raises(ValueError):
        SyncSandboxInstance.create(CONFIG, timeout=51)
