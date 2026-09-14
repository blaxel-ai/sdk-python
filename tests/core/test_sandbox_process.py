from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess


@pytest.mark.asyncio
async def test_async_wait_returns_immediately_for_terminal_initial_status(monkeypatch):
    process = object.__new__(SandboxProcess)
    completed = SimpleNamespace(status="completed")
    get = AsyncMock(return_value=completed)
    sleep = AsyncMock()
    monkeypatch.setattr(process, "get", get)
    monkeypatch.setattr("blaxel.core.sandbox.default.process.asyncio.sleep", sleep)

    assert await process.wait("process-id", interval=5000) is completed
    get.assert_awaited_once_with("process-id")
    sleep.assert_not_awaited()


def test_sync_wait_returns_immediately_for_terminal_initial_status(monkeypatch):
    process = object.__new__(SyncSandboxProcess)
    completed = SimpleNamespace(status="completed")
    get = Mock(return_value=completed)
    sleep = Mock()
    monkeypatch.setattr(process, "get", get)
    monkeypatch.setattr("blaxel.core.sandbox.sync.process.time.sleep", sleep)

    assert process.wait("process-id", interval=5000) is completed
    get.assert_called_once_with("process-id")
    sleep.assert_not_called()
