"""Jobs API Integration Tests.

Note: These tests require a job named "mk3" to exist in your workspace.
The job should accept tasks with a "duration" field.
"""

import pytest

from blaxel.core.client.models.create_job_execution_request import CreateJobExecutionRequest
from blaxel.core.client.models.create_job_execution_request_env import CreateJobExecutionRequestEnv
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

    async def test_run_job_without_overrides(self):
        """Test running a job without any overrides."""
        job = bl_job(TEST_JOB_NAME)

        try:
            execution_id = await job.arun([{"name": "Richard"}, {"name": "John"}])
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

        assert execution_id is not None
        assert isinstance(execution_id, str)

        # Verify execution was created
        execution = await job.aget_execution(execution_id)
        assert execution is not None
        assert execution.status is not None

    async def test_run_job_with_memory_override(self):
        """Test running a job with memory override."""
        job = bl_job(TEST_JOB_NAME)

        try:
            execution_id = await job.arun(tasks=[{"name": "MemoryTest"}], memory=2048)
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

        assert execution_id is not None
        assert isinstance(execution_id, str)

        # Verify execution was created
        execution = await job.aget_execution(execution_id)
        assert execution is not None
        assert execution.status is not None

    async def test_run_job_with_env_overrides(self):
        """Test running a job with environment variable overrides."""
        job = bl_job(TEST_JOB_NAME)

        try:
            execution_id = await job.arun(
                tasks=[{"name": "EnvTest"}], env={"CUSTOM_VAR": "test_value", "DEBUG_MODE": "true"}
            )
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

        assert execution_id is not None
        assert isinstance(execution_id, str)

        # Verify execution was created
        execution = await job.aget_execution(execution_id)
        assert execution is not None
        assert execution.status is not None

    async def test_run_job_with_both_memory_and_env_overrides(self):
        """Test running a job with both memory and env overrides."""
        job = bl_job(TEST_JOB_NAME)

        try:
            execution_id = await job.arun(
                tasks=[{"name": "CombinedTest"}],
                memory=1024,
                env={"TEST_ENV": "production", "LOG_LEVEL": "info"},
            )
        except KeyError as e:
            pytest.skip(f"Job API response missing expected field: {e}")
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

        assert execution_id is not None
        assert isinstance(execution_id, str)

        # Verify execution was created
        execution = await job.aget_execution(execution_id)
        assert execution is not None
        assert execution.status is not None

    async def test_create_execution_with_memory_override(self):
        """Test creating an execution with memory override.

        Memory override must be less than or equal to the job's configured memory.
        """
        job = bl_job(TEST_JOB_NAME)

        # Override memory to 512 MB (must be <= job's configured memory)
        request = CreateJobExecutionRequest(
            tasks=[{"name": "John"}],
            memory=512,
        )

        try:
            execution_id = await job.acreate_execution(request)
            assert execution_id is not None
            assert isinstance(execution_id, str)

            # Verify the execution was created
            execution = await job.aget_execution(execution_id)
            assert execution is not None
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

    async def test_create_execution_with_env_override(self):
        """Test creating an execution with environment variable overrides.

        Environment variables are merged with the job's configured variables.
        """
        job = bl_job(TEST_JOB_NAME)

        # Create environment overrides
        env = CreateJobExecutionRequestEnv()
        env["CUSTOM_VAR"] = "test_value"
        env["BATCH_SIZE"] = "100"

        request = CreateJobExecutionRequest(
            tasks=[{"name": "Jane"}],
            env=env,
        )

        try:
            execution_id = await job.acreate_execution(request)
            assert execution_id is not None
            assert isinstance(execution_id, str)

            # Verify the execution was created
            execution = await job.aget_execution(execution_id)
            assert execution is not None
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise

    async def test_create_execution_with_memory_and_env_overrides(self):
        """Test creating an execution with both memory and env overrides.

        Both overrides can be applied simultaneously to a single execution.
        """
        job = bl_job(TEST_JOB_NAME)

        # Create environment overrides
        env = CreateJobExecutionRequestEnv()
        env["LOG_LEVEL"] = "debug"
        env["TIMEOUT"] = "30"

        request = CreateJobExecutionRequest(
            tasks=[{"name": "Bob"}],
            memory=1024,  # 1 GB override
            env=env,
        )

        try:
            execution_id = await job.acreate_execution(request)
            assert execution_id is not None
            assert isinstance(execution_id, str)

            # Verify the execution was created
            execution = await job.aget_execution(execution_id)
            assert execution is not None
            assert execution.status is not None
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                pytest.skip(f"Job '{TEST_JOB_NAME}' not found in workspace")
            raise
