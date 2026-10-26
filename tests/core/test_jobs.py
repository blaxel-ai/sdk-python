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


def test_select_task_arguments_var_keyword_receives_all():
    """A function declaring **kwargs receives every task argument unchanged."""
    from blaxel.core.jobs import _select_task_arguments

    def catch_all(**kwargs):
        return kwargs

    payload = {"name": "x", "age": 1, "a": "extra"}
    assert _select_task_arguments(catch_all, payload) == payload


def test_select_task_arguments_filters_to_declared_parameters():
    """Only parameters the function declares are forwarded; extras are dropped."""
    from blaxel.core.jobs import _select_task_arguments

    def greet(name, age):
        return (name, age)

    selected = _select_task_arguments(greet, {"name": "x", "age": 1, "a": "extra"})
    assert selected == {"name": "x", "age": 1}


def test_select_task_arguments_keyword_only_parameters():
    """Keyword-only parameters are forwarded, positional-only/unknown keys dropped."""
    from blaxel.core.jobs import _select_task_arguments

    def job(*, name, age=0):
        return (name, age)

    selected = _select_task_arguments(job, {"name": "x", "extra": 1})
    assert selected == {"name": "x"}


def test_select_task_arguments_no_parameters_drops_everything():
    """A zero-argument function receives nothing, no matter the payload."""
    from blaxel.core.jobs import _select_task_arguments

    def job():
        return None

    assert _select_task_arguments(job, {"a": 1, "b": 2}) == {}


def test_select_task_arguments_unintrospectable_callable_passes_through():
    """Callables without an introspectable signature keep the historical behavior."""
    from blaxel.core.jobs import _select_task_arguments

    # ``max`` is a builtin whose signature inspect cannot resolve -> forward all.
    payload = {"a": 1, "b": 2}
    assert _select_task_arguments(max, payload) == payload


def test_bl_start_job_ignores_unexpected_task_arguments(monkeypatch):
    """A task argument the function does not declare must not crash the job.

    Regression for SDK-PYTHON-12V (``TypeError: my_job() got an unexpected keyword
    argument 'a'``). Before the fix this raised SystemExit(1) with a TypeError cause.
    """
    from blaxel.core.jobs import bl_start_job

    monkeypatch.setattr("sys.argv", ["job", "--a", "1"])
    monkeypatch.delenv("BL_EXECUTION_DATA_URL", raising=False)

    calls = []

    def my_job():
        calls.append(True)

    bl_start_job.start(my_job)
    assert calls == [True]


def test_bl_start_job_forwards_declared_arguments(monkeypatch):
    """Declared parameters are forwarded; undeclared payload keys are ignored."""
    from blaxel.core.jobs import bl_start_job

    monkeypatch.setattr("sys.argv", ["job", "--name", "charlou", "--a", "1"])
    monkeypatch.delenv("BL_EXECUTION_DATA_URL", raising=False)

    received = {}

    def greet(name):
        received["name"] = name

    bl_start_job.start(greet)
    assert received == {"name": "charlou"}


def test_bl_start_job_missing_required_argument_still_fails(monkeypatch):
    """A genuinely missing required argument must still fail fast (not be masked)."""
    from blaxel.core.jobs import bl_start_job

    monkeypatch.setattr("sys.argv", ["job"])
    monkeypatch.delenv("BL_EXECUTION_DATA_URL", raising=False)

    def needs_name(name):
        raise AssertionError("should not be called")

    with pytest.raises(SystemExit) as excinfo:
        bl_start_job.start(needs_name)
    assert excinfo.value.code == 1
    assert isinstance(excinfo.value.__cause__, TypeError)
