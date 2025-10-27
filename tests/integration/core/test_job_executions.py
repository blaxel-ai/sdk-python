import asyncio
import time

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.core.client.models.create_job_execution_request import (
    CreateJobExecutionRequest,
)
from blaxel.core.jobs import bl_job

logger = getLogger(__name__)


def test_job_executions_sync():
    """Test job executions using synchronous methods."""
    job_name = "mk3"
    job = bl_job(job_name)

    print(f"Testing job executions for: {job_name}")

    # Create a new execution
    print("\n1. Creating new execution...")
    request = CreateJobExecutionRequest(
        id=f"test-exec-{int(time.time())}",
        tasks=[
            {"duration": 60},
            {"duration": 60},
        ],
    )
    execution_id = job.create_execution(request)
    print(f"✓ Created execution: {execution_id}")

    # Get the execution details
    print("\n2. Getting execution details...")
    execution = job.get_execution(execution_id)
    print(f"✓ Execution status: {execution.status}")
    print(f"✓ Execution metadata: {execution.metadata}")

    # Get just the status
    print("\n3. Getting execution status...")
    status = job.get_execution_status(execution_id)
    print(f"✓ Status: {status}")

    # List all executions
    print("\n4. Listing all executions...")
    executions = job.list_executions(limit=50)
    print(f"✓ Found {len(executions)} execution(s)")

    # Wait for completion (with short timeout for testing)
    print("\n5. Waiting for execution to complete...")
    try:
        completed_execution = job.wait_for_execution(
            execution_id,
            max_wait=300,  # 300 seconds (5 minutes) - accounts for job launch delays
            interval=3,  # 3 seconds
        )
        print(f"✓ Execution completed with status: {completed_execution.status}")
    except Exception as error:
        print(f"⚠ Execution still running or timed out: {error}")

    # Get just the status
    print("\n6. Getting execution status...")
    status = job.get_execution_status(execution_id)
    print(f"✓ Status: {status}")

    print("\n✅ All sync tests completed!")


async def test_job_executions_async():
    """Test job executions using async methods."""
    job_name = "mk3"
    job = bl_job(job_name)

    print(f"\nTesting job executions (async) for: {job_name}")

    # Create a new execution
    print("\n1. Creating new execution (async)...")
    request = CreateJobExecutionRequest(
        id=f"test-exec-async-{int(time.time())}",
        tasks=[
            {"duration": 60},
            {"duration": 60},
        ],
    )
    execution_id = await job.acreate_execution(request)
    print(f"✓ Created execution: {execution_id}")

    # Get the execution details
    print("\n2. Getting execution details (async)...")
    execution = await job.aget_execution(execution_id)
    print(f"✓ Execution status: {execution.status}")
    print(f"✓ Execution metadata: {execution.metadata}")

    # Get just the status
    print("\n3. Getting execution status (async)...")
    status = await job.aget_execution_status(execution_id)
    print(f"✓ Status: {status}")

    # List all executions
    print("\n4. Listing all executions (async)...")
    executions = await job.alist_executions(limit=50)
    print(f"✓ Found {len(executions)} execution(s)")

    # Wait for completion (with short timeout for testing)
    print("\n5. Waiting for execution to complete (async)...")
    try:
        completed_execution = await job.await_for_execution(
            execution_id,
            max_wait=300,  # 300 seconds (5 minutes) - accounts for job launch delays
            interval=3,  # 3 seconds
        )
        print(f"✓ Execution completed with status: {completed_execution.status}")
    except Exception as error:
        print(f"⚠ Execution still running or timed out: {error}")

    # Get just the status
    print("\n6. Getting execution status (async)...")
    status = await job.aget_execution_status(execution_id)
    print(f"✓ Status: {status}")

    print("\n✅ All async tests completed!")


if __name__ == "__main__":
    # Test sync methods
    try:
        test_job_executions_sync()
    except Exception as e:
        logger.error(f"Sync test failed: {e}", exc_info=True)
        print(f"\n❌ Sync test failed: {e}")

    # Test async methods
    try:
        asyncio.run(test_job_executions_async())
    except Exception as e:
        logger.error(f"Async test failed: {e}", exc_info=True)
        print(f"\n❌ Async test failed: {e}")
