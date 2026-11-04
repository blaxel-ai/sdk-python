import argparse
import asyncio
import inspect
import os
import time
from logging import getLogger
from typing import Any, Callable, Dict, List

import requests

from ..client import client
from ..client.api.jobs import (
    create_job_execution,
    delete_job_execution,
    get_job_execution,
    list_job_executions,
)
from ..client.models.create_job_execution_request import (
    CreateJobExecutionRequest,
)
from ..client.models.job_execution import JobExecution
from ..client.pagination import (
    AsyncPaginatedList,
    PaginatedList,
    make_async_paginated_list,
    make_paginated_list,
    normalize_cursor,
)


def _select_task_arguments(func: Callable, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Return the subset of task arguments ``func`` accepts as keyword arguments.

    A task payload is forwarded to the job function as keyword arguments. When the
    function declares ``**kwargs`` it receives every argument unchanged. Otherwise
    only the parameters it explicitly declares are forwarded, so extra keys in the
    payload (a typo, a field another task needs, or a platform-injected field) do
    not crash the whole job with
    ``TypeError: <func>() got an unexpected keyword argument``. This mirrors the
    TypeScript SDK, which hands the function a single arguments object and simply
    ignores properties it does not read.
    """
    try:
        signature = inspect.signature(func)
    except (TypeError, ValueError):
        # Builtins / C-level callables without an introspectable signature: keep
        # the historical behavior and forward every argument.
        return arguments

    parameters = signature.parameters.values()
    if any(parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in parameters):
        return arguments

    accepted = {
        name
        for name, parameter in signature.parameters.items()
        if parameter.kind
        in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
    }
    selected = {key: value for key, value in arguments.items() if key in accepted}

    ignored = sorted(set(arguments) - set(selected))
    if ignored:
        logger.debug(
            "Ignoring job task argument(s) not accepted by %s: %s",
            getattr(func, "__name__", repr(func)),
            ", ".join(ignored),
        )
    return selected


class BlJobWrapper:
    def get_arguments(self) -> Dict[str, Any]:
        if not os.getenv("BL_EXECUTION_DATA_URL"):
            parser = argparse.ArgumentParser()
            # Parse known args, ignore unknown
            args, unknown = parser.parse_known_args()
            # Convert to dict and include unknown args
            args_dict = vars(args)
            # Add unknown args to dict
            for i in range(0, len(unknown), 2):
                if i + 1 < len(unknown):
                    key = unknown[i].lstrip("-")
                    args_dict[key] = unknown[i + 1]
            return args_dict

        response = requests.get(os.getenv("BL_EXECUTION_DATA_URL") or "")
        data = response.json()
        tasks = data.get("tasks", [])
        return tasks[self.index] if self.index < len(tasks) else {}

    @property
    def index_key(self) -> str:
        return os.getenv("BL_TASK_KEY", "TASK_INDEX")

    @property
    def index(self) -> int:
        index_value = os.getenv(self.index_key)
        return int(index_value) if index_value else 0

    def start(self, func: Callable):
        """
        Run a job defined in a function, it's run in the current process.
        Handles both async and sync functions.
        Arguments are passed as keyword arguments to the function. Task-payload
        keys the function does not declare are ignored (unless it accepts
        ``**kwargs``), so extra or platform-injected fields do not crash the job.
        """
        try:
            parsed_args = self.get_arguments()
            call_args = _select_task_arguments(func, parsed_args)
            if asyncio.iscoroutinefunction(func):
                asyncio.run(func(**call_args))
            else:
                func(**call_args)
        except Exception as error:
            logger.error(f"Job execution failed: {error}")
            raise SystemExit(1) from error


logger = getLogger(__name__)


class BlJob:
    def __init__(self, name: str):
        self.name = name

    def run(
        self,
        tasks: List[Dict[str, Any]],
        env: Dict[str, str] | None = None,
        memory: int | None = None,
        execution_id: str | None = None,
        allow_queue: bool | None = None,
    ) -> str:
        """
        Run the job with the provided tasks and optional overrides.

        Args:
            tasks: List of task parameters for parallel execution
            env: Optional environment variable overrides (merged with job's environment)
            memory: Optional memory override in megabytes (must be <= job's configured memory)
            execution_id: Optional custom execution ID
            allow_queue: When False, capacity is checked synchronously and the request is
                rejected immediately with a 429 error if the execution cannot start right
                now, instead of being queued and retried in the background. Omitted or
                True keeps the queue-and-retry behavior.

        Returns:
            str: The execution ID

        Raises:
            Exception: If the job execution fails
        """
        logger.debug(f"Job Calling: {self.name}")

        request = CreateJobExecutionRequest(tasks=tasks)
        if env is not None:
            request.env = env
        if memory is not None:
            request.memory = memory
        if execution_id is not None:
            request.execution_id = execution_id
        if allow_queue is not None:
            request.allow_queue = allow_queue

        return self.create_execution(request)

    async def arun(
        self,
        tasks: List[Dict[str, Any]],
        env: Dict[str, str] | None = None,
        memory: int | None = None,
        execution_id: str | None = None,
        allow_queue: bool | None = None,
    ) -> str:
        """
        Run the job with the provided tasks and optional overrides (async).

        Args:
            tasks: List of task parameters for parallel execution
            env: Optional environment variable overrides (merged with job's environment)
            memory: Optional memory override in megabytes (must be <= job's configured memory)
            execution_id: Optional custom execution ID
            allow_queue: When False, capacity is checked synchronously and the request is
                rejected immediately with a 429 error if the execution cannot start right
                now, instead of being queued and retried in the background. Omitted or
                True keeps the queue-and-retry behavior.

        Returns:
            str: The execution ID

        Raises:
            Exception: If the job execution fails
        """
        logger.debug(f"Job Calling: {self.name}")

        request = CreateJobExecutionRequest(tasks=tasks)
        if env is not None:
            request.env = env
        if memory is not None:
            request.memory = memory
        if execution_id is not None:
            request.execution_id = execution_id
        if allow_queue is not None:
            request.allow_queue = allow_queue

        return await self.acreate_execution(request)

    def create_execution(self, request: CreateJobExecutionRequest) -> str:
        """
        Create a new execution for this job and return the execution ID.

        Args:
            request: The job execution request containing tasks and optional execution ID

        Returns:
            str: The execution ID

        Raises:
            Exception: If no execution ID is returned or the request fails
        """
        logger.debug(f"Creating execution for job: {self.name}")

        response = create_job_execution.sync_detailed(
            job_id=self.name,
            client=client,
            body=request,
        )

        if response.status_code != 200:
            raise Exception(f"Failed to create job execution: {response.status_code}")

        # The API returns executionId at the root level
        if response.parsed and hasattr(response.parsed, "to_dict"):
            response_dict = response.parsed.to_dict()
        else:
            # Parse the raw response to get executionId
            import json

            response_dict = json.loads(response.content)

        # Check for both camelCase (API) and snake_case (parsed) formats
        execution_id = response_dict.get("execution_id") or response_dict.get("executionId")
        if not execution_id:
            raise Exception("No execution ID returned from create job execution")

        logger.debug(f"Created execution: {execution_id}")
        return execution_id

    async def acreate_execution(self, request: CreateJobExecutionRequest) -> str:
        """
        Create a new execution for this job and return the execution ID (async).

        Args:
            request: The job execution request containing tasks and optional execution ID

        Returns:
            str: The execution ID

        Raises:
            Exception: If no execution ID is returned or the request fails
        """
        logger.debug(f"Creating execution for job: {self.name}")

        response = await create_job_execution.asyncio_detailed(
            job_id=self.name,
            client=client,
            body=request,
        )
        if response.status_code != 200:
            raise Exception(f"Failed to create job execution: {response.status_code}")

        # The API returns executionId at the root level
        if response.parsed and hasattr(response.parsed, "to_dict"):
            response_dict = response.parsed.to_dict()
        else:
            # Parse the raw response to get executionId
            import json

            response_dict = json.loads(response.content)

        # Check for both camelCase (API) and snake_case (parsed) formats
        execution_id = response_dict.get("execution_id") or response_dict.get("executionId")
        if not execution_id:
            raise Exception("No execution ID returned from create job execution")

        logger.debug(f"Created execution: {execution_id}")
        return execution_id

    def get_execution(self, execution_id: str) -> JobExecution:
        """
        Get a specific execution by ID.

        Args:
            execution_id: The execution ID

        Returns:
            JobExecution: The execution object

        Raises:
            Exception: If the execution is not found or the request fails
        """
        logger.debug(f"Getting execution {execution_id} for job: {self.name}")

        response = get_job_execution.sync_detailed(
            job_id=self.name,
            execution_id=execution_id,
            client=client,
        )

        if response.status_code == 404:
            raise Exception(f"Execution '{execution_id}' not found for job '{self.name}'")

        if response.status_code != 200:
            raise Exception(f"Failed to get job execution: {response.status_code}")

        if not response.parsed:
            raise Exception("No execution data returned")

        return response.parsed

    async def aget_execution(self, execution_id: str) -> JobExecution:
        """
        Get a specific execution by ID (async).

        Args:
            execution_id: The execution ID

        Returns:
            JobExecution: The execution object

        Raises:
            Exception: If the execution is not found or the request fails
        """
        logger.debug(f"Getting execution {execution_id} for job: {self.name}")

        response = await get_job_execution.asyncio_detailed(
            job_id=self.name,
            execution_id=execution_id,
            client=client,
        )

        if response.status_code == 404:
            raise Exception(f"Execution '{execution_id}' not found for job '{self.name}'")

        if response.status_code != 200:
            raise Exception(f"Failed to get job execution: {response.status_code}")

        if not response.parsed:
            raise Exception("No execution data returned")

        return response.parsed

    def list_executions(
        self, limit: int = 20, offset: int = 0, cursor: str | None = None
    ) -> PaginatedList[JobExecution]:
        """
        List executions for this job.

        Args:
            limit: Maximum number of executions to return per page
            offset: Legacy offset for older API versions
            cursor: Starting cursor

        Returns:
            PaginatedList[JobExecution]: Page of execution objects

        Example:
            ```python
            page = bl_job("my-job").list_executions(limit=20)

            for execution in page.data:
                print(execution.metadata.id)

            if page.has_more:
                next_page = page.next_page()

            for execution in page.auto_paging_iter():
                print(execution.metadata.id)
            ```
        """
        logger.debug(f"Listing executions for job: {self.name}")

        def fetch_page(page_cursor: str | None):
            response = list_job_executions.sync_detailed(
                job_id=self.name,
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
                offset=offset if page_cursor is None else 0,
            )

            if response.status_code != 200:
                raise Exception(f"Failed to list job executions: {response.status_code}")
            return make_paginated_list(
                response.parsed, mapper=lambda execution: execution, fetch_next=fetch_page
            )

        return fetch_page(cursor)

    async def alist_executions(
        self, limit: int = 20, offset: int = 0, cursor: str | None = None
    ) -> AsyncPaginatedList[JobExecution]:
        """
        List executions for this job (async).

        Args:
            limit: Maximum number of executions to return per page
            offset: Legacy offset for older API versions
            cursor: Starting cursor

        Returns:
            AsyncPaginatedList[JobExecution]: Page of execution objects

        Example:
            ```python
            page = await bl_job("my-job").alist_executions(limit=20)

            for execution in page.data:
                print(execution.metadata.id)

            if page.has_more:
                next_page = await page.next_page()

            async for execution in page.auto_paging_iter():
                print(execution.metadata.id)
            ```
        """
        logger.debug(f"Listing executions for job: {self.name}")

        async def fetch_page(page_cursor: str | None):
            response = await list_job_executions.asyncio_detailed(
                job_id=self.name,
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
                offset=offset if page_cursor is None else 0,
            )

            if response.status_code != 200:
                raise Exception(f"Failed to list job executions: {response.status_code}")
            return make_async_paginated_list(
                response.parsed, mapper=lambda execution: execution, fetch_next=fetch_page
            )

        return await fetch_page(cursor)

    def get_execution_status(self, execution_id: str) -> str:
        """
        Get the status of a specific execution.

        Args:
            execution_id: The execution ID

        Returns:
            str: The execution status
        """
        execution = self.get_execution(execution_id)
        return execution.status if execution.status else "UNKNOWN"

    async def aget_execution_status(self, execution_id: str) -> str:
        """
        Get the status of a specific execution (async).

        Args:
            execution_id: The execution ID

        Returns:
            str: The execution status
        """
        execution = await self.aget_execution(execution_id)
        return execution.status if execution.status else "UNKNOWN"

    def cancel_execution(self, execution_id: str) -> None:
        """
        Cancel a specific execution.

        Args:
            execution_id: The execution ID

        Raises:
            Exception: If the cancellation fails
        """
        logger.debug(f"Cancelling execution {execution_id} for job: {self.name}")

        response = delete_job_execution.sync_detailed(
            job_id=self.name,
            execution_id=execution_id,
            client=client,
        )

        if response.status_code != 200:
            raise Exception(f"Failed to cancel job execution: {response.status_code}")

    async def acancel_execution(self, execution_id: str) -> None:
        """
        Cancel a specific execution (async).

        Args:
            execution_id: The execution ID

        Raises:
            Exception: If the cancellation fails
        """
        logger.debug(f"Cancelling execution {execution_id} for job: {self.name}")

        response = await delete_job_execution.asyncio_detailed(
            job_id=self.name,
            execution_id=execution_id,
            client=client,
        )

        if response.status_code != 200:
            raise Exception(f"Failed to cancel job execution: {response.status_code}")

    def wait_for_execution(
        self,
        execution_id: str,
        max_wait: int = 360,
        interval: int = 3,
    ) -> JobExecution:
        """
        Wait for an execution to complete.

        Args:
            execution_id: The execution ID to wait for
            max_wait: Maximum time to wait in seconds (default: 360 = 6 minutes)
            interval: Polling interval in seconds (default: 3 seconds)

        Returns:
            JobExecution: The completed execution

        Raises:
            Exception: If the execution doesn't complete within max_wait seconds
        """
        logger.debug(f"Waiting for execution {execution_id} to complete (max {max_wait}s)")

        start_time = time.time()

        while time.time() - start_time < max_wait:
            execution = self.get_execution(execution_id)
            status = execution.status

            # Terminal states (Kubernetes-style: succeeded, failed, cancelled)
            if status in ["succeeded", "failed", "cancelled"]:
                logger.debug(f"Execution {execution_id} finished with status: {status}")
                return execution

            # Wait before polling again
            time.sleep(interval)

        raise Exception(f"Execution {execution_id} did not complete within {max_wait}s")

    async def await_for_execution(
        self,
        execution_id: str,
        max_wait: int = 360,
        interval: int = 3,
    ) -> JobExecution:
        """
        Wait for an execution to complete (async).

        Args:
            execution_id: The execution ID to wait for
            max_wait: Maximum time to wait in seconds (default: 360 = 6 minutes)
            interval: Polling interval in seconds (default: 3 seconds)

        Returns:
            JobExecution: The completed execution

        Raises:
            Exception: If the execution doesn't complete within max_wait seconds
        """
        logger.debug(f"Waiting for execution {execution_id} to complete (max {max_wait}s)")

        start_time = time.time()

        while time.time() - start_time < max_wait:
            execution = await self.aget_execution(execution_id)
            status = execution.status

            # Terminal states (Kubernetes-style: succeeded, failed, cancelled)
            if status in ["succeeded", "failed", "cancelled"]:
                logger.debug(f"Execution {execution_id} finished with status: {status}")
                return execution

            # Wait before polling again
            await asyncio.sleep(interval)

        raise Exception(f"Execution {execution_id} did not complete within {max_wait}s")

    def __str__(self):
        return f"Job {self.name}"

    def __repr__(self):
        return self.__str__()


def bl_job(name: str):
    return BlJob(name)


# Create a singleton instance
bl_start_job = BlJobWrapper()
