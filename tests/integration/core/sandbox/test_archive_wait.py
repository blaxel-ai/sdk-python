"""Tests for archiving and unarchiving a sandbox."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.client.models import Error, Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import SandboxAPIError, SandboxInstance, SyncSandboxInstance


def sandbox(status: str, name: str = "test-sandbox") -> Sandbox:
    record = Sandbox(metadata=Metadata(name=name), spec=SandboxSpec())
    record.status = status
    return record


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_waits_until_the_filesystem_is_stored(mock_archive, mock_get):
    mock_archive.return_value = sandbox("ARCHIVING")
    mock_get.side_effect = [sandbox("ARCHIVING"), sandbox("ARCHIVED")]
    instance = SandboxInstance(sandbox("DEPLOYED"))

    result = await instance.archive(interval=0)

    assert result is instance
    assert instance.status == "ARCHIVED"
    assert instance.config.sandbox is instance.sandbox
    assert mock_get.await_count == 2
    assert mock_archive.call_args.args[0] == "test-sandbox"


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_returns_the_launched_archive_when_not_waiting(mock_archive, mock_get):
    mock_archive.return_value = sandbox("ARCHIVING")
    instance = SandboxInstance(sandbox("DEPLOYED"))

    await instance.archive(wait=False)

    assert instance.status == "ARCHIVING"
    mock_get.assert_not_called()


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_raises_when_the_sandbox_leaves_the_archive(mock_archive, mock_get):
    mock_archive.return_value = sandbox("ARCHIVING")
    # A failed export gives the sandbox back, so it stops archiving without ever
    # reaching ARCHIVED.
    mock_get.return_value = sandbox("FAILED")
    instance = SandboxInstance(sandbox("DEPLOYED"))

    with pytest.raises(SandboxAPIError, match="FAILED"):
        await instance.archive(interval=0)


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_tolerates_the_status_it_starts_from(mock_archive, mock_get):
    # The export is launched before the record moves, so the sandbox is still
    # read as DEPLOYED for a moment.
    mock_archive.return_value = sandbox("DEPLOYED")
    mock_get.side_effect = [sandbox("DEPLOYED"), sandbox("ARCHIVING"), sandbox("ARCHIVED")]
    instance = SandboxInstance(sandbox("DEPLOYED"))

    await instance.archive(interval=0)

    assert instance.status == "ARCHIVED"


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_fails_when_the_sandbox_is_given_back_deployed(mock_archive, mock_get):
    # A failed export hands the sandbox back as DEPLOYED: once it has started
    # archiving, reading DEPLOYED again means it is over, not still running.
    mock_archive.return_value = sandbox("ARCHIVING")
    mock_get.side_effect = [sandbox("ARCHIVING"), sandbox("DEPLOYED")]
    instance = SandboxInstance(sandbox("DEPLOYED"))

    with pytest.raises(SandboxAPIError, match="DEPLOYED"):
        await instance.archive(interval=0)


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.unarchive_sandbox", new_callable=AsyncMock)
async def test_unarchive_fails_when_the_sandbox_stays_archived(mock_unarchive, mock_get):
    mock_unarchive.return_value = sandbox("UNARCHIVING")
    mock_get.side_effect = [sandbox("UNARCHIVING"), sandbox("ARCHIVED")]

    with pytest.raises(SandboxAPIError, match="ARCHIVED"):
        await SandboxInstance.unarchive("test-sandbox", interval=0)


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_gives_up_once_the_timeout_is_spent(mock_archive, mock_get):
    mock_archive.return_value = sandbox("ARCHIVING")
    mock_get.return_value = sandbox("ARCHIVING")
    instance = SandboxInstance(sandbox("DEPLOYED"))

    with pytest.raises(SandboxAPIError, match="still ARCHIVING"):
        await instance.archive(max_wait=0, interval=0)


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_does_not_wait_for_the_first_move_past_the_timeout(mock_archive, mock_get):
    # A sandbox that never leaves DEPLOYED is tolerated only while the caller is
    # still waiting, not for the whole grace period.
    mock_archive.return_value = sandbox("DEPLOYED")
    mock_get.return_value = sandbox("DEPLOYED")
    instance = SandboxInstance(sandbox("DEPLOYED"))

    with pytest.raises(SandboxAPIError, match="DEPLOYED"):
        await instance.archive(max_wait=0, interval=0)

    assert mock_get.await_count == 1


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.get_sandbox", new_callable=AsyncMock)
@patch("blaxel.core.sandbox.default.sandbox.unarchive_sandbox", new_callable=AsyncMock)
async def test_unarchive_can_be_called_on_the_class_with_a_name(mock_unarchive, mock_get):
    mock_unarchive.return_value = sandbox("UNARCHIVING")
    mock_get.side_effect = [sandbox("UNARCHIVING"), sandbox("DEPLOYED")]

    result = await SandboxInstance.unarchive("test-sandbox", interval=0)

    assert isinstance(result, SandboxInstance)
    assert result.status == "DEPLOYED"
    assert mock_unarchive.call_args.args[0] == "test-sandbox"


@pytest.mark.asyncio
@patch("blaxel.core.sandbox.default.sandbox.archive_sandbox", new_callable=AsyncMock)
async def test_archive_raises_on_an_error_response(mock_archive):
    mock_archive.return_value = Error(error="conflict", code=409, message="already archived")
    instance = SandboxInstance(sandbox("ARCHIVED"))

    with pytest.raises(SandboxAPIError):
        await instance.archive()


@patch("blaxel.core.sandbox.sync.sandbox.get_sandbox", new_callable=MagicMock)
@patch("blaxel.core.sandbox.sync.sandbox.archive_sandbox", new_callable=MagicMock)
def test_sync_archive_waits_until_the_filesystem_is_stored(mock_archive, mock_get):
    mock_archive.return_value = sandbox("ARCHIVING")
    mock_get.side_effect = [sandbox("ARCHIVING"), sandbox("ARCHIVED")]
    instance = SyncSandboxInstance(sandbox("DEPLOYED"))

    result = instance.archive(interval=0)

    assert result is instance
    assert instance.status == "ARCHIVED"


@patch("blaxel.core.sandbox.sync.sandbox.get_sandbox", new_callable=MagicMock)
@patch("blaxel.core.sandbox.sync.sandbox.unarchive_sandbox", new_callable=MagicMock)
def test_sync_unarchive_can_be_called_on_the_class_with_a_name(mock_unarchive, mock_get):
    mock_unarchive.return_value = sandbox("UNARCHIVING")
    mock_get.return_value = sandbox("DEPLOYED")

    result = SyncSandboxInstance.unarchive("test-sandbox", interval=0)

    assert isinstance(result, SyncSandboxInstance)
    assert result.status == "DEPLOYED"
    assert mock_unarchive.call_args.args[0] == "test-sandbox"
