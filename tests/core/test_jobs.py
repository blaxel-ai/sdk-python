"""Tests for jobs functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core.jobs import bl_job


@pytest.mark.asyncio
async def test_bl_job_creation():
    """Test job creation."""
    job = bl_job("test-job")
    assert job.name == "test-job"
    assert str(job) == "Job test-job"


@pytest.mark.asyncio
async def test_bl_job_properties():
    """Test job properties."""
    job = bl_job("myjob")

    # Test that core properties are accessible
    assert hasattr(job, "name")
    assert job.name == "myjob"


@pytest.mark.asyncio
@patch("blaxel.core.jobs.create_job_execution")
async def test_bl_job_run(mock_create_job_execution):
    """Test job run functionality."""
    import json

    # Mock sync response
    mock_sync_response = MagicMock()
    mock_sync_response.status_code = 200
    mock_sync_response.content = json.dumps({"executionId": "exec-123"}).encode()
    mock_sync_response.parsed = None
    mock_create_job_execution.sync_detailed.return_value = mock_sync_response

    # Mock async response
    mock_async_response = MagicMock()
    mock_async_response.status_code = 200
    mock_async_response.content = json.dumps({"executionId": "exec-456"}).encode()
    mock_async_response.parsed = None
    mock_create_job_execution.asyncio_detailed = AsyncMock(return_value=mock_async_response)

    job = bl_job("test-job")

    # Test sync run
    result = job.run([{"name": "charlou", "age": 25}])
    assert result == "exec-123"

    # Test async run
    result = await job.arun([{"name": "charlou", "age": 25}])
    assert result == "exec-456"


@pytest.mark.asyncio
async def test_bl_job_methods():
    """Test job has required methods."""
    job = bl_job("test-job")

    # Test that core methods exist
    assert hasattr(job, "run")
    assert hasattr(job, "arun")
    assert hasattr(job, "create_execution")
    assert hasattr(job, "acreate_execution")


@pytest.mark.asyncio
async def test_bl_job_representation():
    """Test job string representation."""
    job = bl_job("test-job")

    # Test string representation
    assert str(job) == "Job test-job"
    assert repr(job) == "Job test-job"


def test_bl_start_job_success_returns_normally(monkeypatch):
    """A task that completes must not raise."""
    from blaxel.core.jobs import bl_start_job

    monkeypatch.setattr("sys.argv", ["job"])
    monkeypatch.delenv("BL_EXECUTION_DATA_URL", raising=False)

    calls = []
    bl_start_job.start(lambda **kwargs: calls.append(kwargs))
    assert calls == [{}]


def test_bl_start_job_failure_exits_nonzero(monkeypatch):
    """A task that raises must exit the job process with a non-zero code (ENG-4261)."""
    from blaxel.core.jobs import bl_start_job

    monkeypatch.setattr("sys.argv", ["job"])
    monkeypatch.delenv("BL_EXECUTION_DATA_URL", raising=False)

    def boom(**kwargs):
        raise RuntimeError("task failed")

    with pytest.raises(SystemExit) as excinfo:
        bl_start_job.start(boom)
    assert excinfo.value.code == 1
    assert isinstance(excinfo.value.__cause__, RuntimeError)
