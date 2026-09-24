"""Unit tests for the SDK-managed ``retry`` on SandboxInstance.create.

``retry=n`` re-issues the creation up to ``n`` more times, only after a creation
timeout (408 / ``CREATION_TIMEOUT``) and only when ``timeout`` is set; every other
error is raised as is.
"""

import json
from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core import (
    SandboxAPIError,
    SandboxCreationTimeoutError,
    SandboxInstance,
    SyncSandboxInstance,
)
from blaxel.core.client import errors as client_errors
from blaxel.core.client.models import Metadata, Sandbox, SandboxRuntime, SandboxSpec
from blaxel.core.client.models.sandbox_error import SandboxError
from blaxel.core.sandbox.default.sandbox import CREATION_TIMEOUT_HEADER

ASYNC_CREATE = "blaxel.core.sandbox.default.sandbox.create_sandbox"
SYNC_CREATE = "blaxel.core.sandbox.sync.sandbox.create_sandbox"
CONFIG = {"name": "retried", "region": "us-pdx-1"}


def _created() -> Sandbox:
    return Sandbox(
        metadata=Metadata(name="retried"),
        spec=SandboxSpec(runtime=SandboxRuntime(image="blaxel/base-image:latest")),
    )


def _timeout_408() -> client_errors.UnexpectedStatus:
    body = {"code": "CREATION_TIMEOUT", "message": "sandbox not ready in time"}
    return client_errors.UnexpectedStatus(408, json.dumps(body).encode())


@pytest.mark.asyncio
async def test_retry_requires_timeout():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        with pytest.raises(ValueError, match="requires 'timeout'"):
            await SandboxInstance.create(CONFIG, retry=1)
        mock_create.assert_not_awaited()


@pytest.mark.parametrize("retry", [-1, 1.5, True, "2"])
@pytest.mark.asyncio
async def test_retry_must_be_a_non_negative_integer(retry):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        with pytest.raises(ValueError, match="non-negative whole number"):
            await SandboxInstance.create(CONFIG, timeout=10, retry=retry)
        mock_create.assert_not_awaited()


@pytest.mark.asyncio
async def test_retries_after_creation_timeouts_until_success():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_timeout_408(), _timeout_408(), _created()]

        result = await SandboxInstance.create(CONFIG, timeout=10, retry=2)

        assert result.metadata.name == "retried"
        assert mock_create.await_count == 3
        for call in mock_create.await_args_list:
            assert call.kwargs["client"]._headers[CREATION_TIMEOUT_HEADER] == "10"
            assert call.kwargs["body"] == mock_create.await_args_list[0].kwargs["body"]


@pytest.mark.asyncio
async def test_raises_after_the_retry_budget_is_exhausted():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_timeout_408(), _timeout_408(), _timeout_408()]

        with pytest.raises(SandboxCreationTimeoutError) as excinfo:
            await SandboxInstance.create(CONFIG, timeout=10, retry=2)

        assert mock_create.await_count == 3
        assert excinfo.value.timeout == 10
        assert excinfo.value.sandbox_name == "retried"


@pytest.mark.asyncio
async def test_no_retry_by_default_and_with_retry_zero():
    for kwargs in ({}, {"retry": 0}):
        with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = _timeout_408()
            with pytest.raises(SandboxCreationTimeoutError):
                await SandboxInstance.create(CONFIG, timeout=10, **kwargs)
            mock_create.assert_awaited_once()


@pytest.mark.asyncio
async def test_only_creation_timeouts_are_retried():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = SandboxError(code="QUOTA", message="nope", status_code=403)
        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG, timeout=10, retry=3)
        assert not isinstance(excinfo.value, SandboxCreationTimeoutError)
        mock_create.assert_awaited_once()

    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = client_errors.UnexpectedStatus(502, b"bad gateway")
        with pytest.raises(client_errors.UnexpectedStatus):
            await SandboxInstance.create(CONFIG, timeout=10, retry=3)
        mock_create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_if_not_exists_forwards_retry():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_timeout_408(), _created()]

        result = await SandboxInstance.create_if_not_exists(CONFIG, timeout=10, retry=1)

        assert result.metadata.name == "retried"
        assert mock_create.await_count == 2
        assert all(c.kwargs["create_if_not_exist"] is True for c in mock_create.await_args_list)

    with pytest.raises(ValueError, match="requires 'timeout'"):
        await SandboxInstance.create_if_not_exists(CONFIG, retry=1)


def test_sync_retry():
    with patch(SYNC_CREATE) as mock_create:
        mock_create.side_effect = [_timeout_408(), _created()]
        result = SyncSandboxInstance.create(CONFIG, timeout=10, retry=1)
        assert result.metadata.name == "retried"
        assert mock_create.call_count == 2

    with patch(SYNC_CREATE) as mock_create:
        mock_create.side_effect = [_timeout_408(), _timeout_408()]
        with pytest.raises(SandboxCreationTimeoutError):
            SyncSandboxInstance.create_if_not_exists(CONFIG, timeout=10, retry=1)
        assert mock_create.call_count == 2

    with pytest.raises(ValueError, match="requires 'timeout'"):
        SyncSandboxInstance.create(CONFIG, retry=1)
