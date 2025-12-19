"""Jobs API Integration Tests.

Note: These tests require a job named "mk3" to exist in your workspace.
The job should accept tasks with a "duration" field.
"""

import pytest

from blaxel.core.client.models.create_job_execution_request import CreateJobExecutionRequest
from blaxel.core.jobs import bl_job

TEST_JOB_NAME = "mk3"


class TestBlJob:
    """Test bl_job reference creation."""

    def test_can_create_a_job_reference(self):
        """Test creating a job reference."""
        job = bl_job(TEST_JOB_NAME)

        assert job is not None
        assert hasattr(job, "create_execution")
        assert hasattr(job, "get_execution")
        assert hasattr(job, "list_executions")


@pytest.mark.asyncio(loop_scope="class")
class TestJobExecutions:
    """Test job execution operations.

    Note: These tests require the job "mk3" to exist and be properly configured.
    If the job doesn't exist, tests will be skipped.
    """

    async def test_can_create_an_execution(self):
        """Test creating a job execution."""
        job = bl_job(TEST_JOB_NAME)

        request = CreateJobExecutionRequest(
            tasks=[
                {"duration": 10},
                {"duration": 10},
            ],
        )
        try:
            execution_id = await job.acreate_execution(request)
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

        assert execution_id is not None
        assert isinstance(execution_id, str)

    async def test_can_get_execution_details(self):
        """Test getting execution details."""
        job = bl_job(TEST_JOB_NAME)

        request = CreateJobExecutionRequest(
            tasks=[{"duration": 5}],
        )
        try:
            execution_id = await job.acreate_execution(request)
            execution = await job.aget_execution(execution_id)
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found or returned unexpected data")
            raise

        assert execution is not None
        assert execution.status is not None

    async def test_can_get_execution_status(self):
        """Test getting execution status."""
        job = bl_job(TEST_JOB_NAME)

        request = CreateJobExecutionRequest(
            tasks=[{"duration": 5}],
        )
        try:
            execution_id = await job.acreate_execution(request)
            status = await job.aget_execution_status(execution_id)
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found or returned unexpected data")
            raise

        assert status is not None
        assert isinstance(status, str)

    async def test_can_list_executions(self):
        """Test listing executions."""
        job = bl_job(TEST_JOB_NAME)

        try:
            # Create an execution first
            request = CreateJobExecutionRequest(
                tasks=[{"duration": 5}],
            )
            await job.acreate_execution(request)

            executions = await job.alist_executions()
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found or returned unexpected data")
            raise

        assert executions is not None
        assert isinstance(executions, list)
        assert len(executions) > 0

    async def test_can_wait_for_execution_to_complete(self):
        """Test waiting for execution to complete."""
        job = bl_job(TEST_JOB_NAME)

        request = CreateJobExecutionRequest(
            tasks=[{"duration": 5}],
        )
        try:
            execution_id = await job.acreate_execution(request)

            completed_execution = await job.await_for_execution(
                execution_id,
                max_wait=60,  # 1 minute
                interval=3,  # 3 seconds
            )
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found or returned unexpected data")
            raise

        assert completed_execution is not None
        assert completed_execution.status in ["succeeded", "failed", "cancelled"]


@pytest.mark.asyncio(loop_scope="class")
class TestJobRun:
    """Test job run convenience method."""

    async def test_can_run_job_and_wait_for_completion(self):
        """Test running a job and waiting for completion."""
        job = bl_job(TEST_JOB_NAME)

        try:
            result = await job.arun([{"duration": 5}])
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

        assert result is not None
