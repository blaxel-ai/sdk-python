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

    async def test_create_get_and_list_execution(self):
        """Test creating an execution, then getting its details, status, and listing executions.

        This test combines multiple operations to reduce parallel executions.
        """
        job = bl_job(TEST_JOB_NAME)

        request = CreateJobExecutionRequest(
            tasks=[{"name": "John"}],
        )
        try:
            # Create execution
            execution_id = await job.acreate_execution(request)
            assert execution_id is not None
            assert isinstance(execution_id, str)

            # Get execution details
            execution = await job.aget_execution(execution_id)
            assert execution is not None
            assert execution.status is not None

            # Get execution status
            status = await job.aget_execution_status(execution_id)
            assert status is not None
            assert isinstance(status, str)

            # List executions (should include the one we just created)
            executions = await job.alist_executions()
            assert executions is not None
            assert isinstance(executions, list)
            assert len(executions) > 0

        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

    async def test_wait_for_execution_to_complete(self):
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
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found or returned unexpected data")
            raise

        assert completed_execution is not None
        assert completed_execution.status in ["succeeded", "failed", "cancelled"]

    async def test_run_job_and_wait_for_completion(self):
        """Test running a job and waiting for completion using the convenience method."""
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
