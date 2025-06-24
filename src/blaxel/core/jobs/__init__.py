import argparse
import asyncio
import os
import sys
from logging import getLogger
from typing import Any, Awaitable, Callable, Dict

import requests

from ..client import client
from ..common.internal import get_forced_url, get_global_unique_hash
from ..common.settings import settings


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

        response = requests.get(os.getenv("BL_EXECUTION_DATA_URL"))
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
        Arguments are passed as keyword arguments to the function.
        """
        try:
            parsed_args = self.get_arguments()
            if asyncio.iscoroutinefunction(func):
                asyncio.run(func(**parsed_args))
            else:
                func(**parsed_args)
        except Exception as error:
            print("Job execution failed:", error, file=sys.stderr)
            sys.exit(1)


logger = getLogger(__name__)


class BlJob:
    def __init__(self, name: str):
        self.name = name

    @property
    def internal_url(self):
        """Get the internal URL for the job using a hash of workspace and job name."""
        hash = get_global_unique_hash(settings.workspace, "job", self.name)
        return f"{settings.run_internal_protocol}://bl-{settings.env}-{hash}.{settings.run_internal_hostname}"

    @property
    def forced_url(self):
        """Get the forced URL from environment variables if set."""
        return get_forced_url("job", self.name)

    @property
    def external_url(self):
        return f"{settings.run_url}/{settings.workspace}/jobs/{self.name}"

    @property
    def fallback_url(self):
        if self.external_url != self.url:
            return self.external_url
        return None

    @property
    def url(self):
        if self.forced_url:
            return self.forced_url
        if settings.run_internal_hostname:
            return self.internal_url
        return self.external_url

    def call(self, url, input_data, headers: dict = {}, params: dict = {}):
        body = {"tasks": input_data}

        return client.get_httpx_client().post(
            url + "/executions",
            headers={"Content-Type": "application/json", **headers},
            json=body,
            params=params,
        )

    async def acall(self, url, input_data, headers: dict = {}, params: dict = {}):
        logger.debug(f"Job Calling: {self.name}")
        body = {"tasks": input_data}

        return await client.get_async_httpx_client().post(
            url + "/executions",
            headers={"Content-Type": "application/json", **headers},
            json=body,
            params=params,
        )

    def run(self, input: Any, headers: dict = {}, params: dict = {}) -> str:
        logger.debug(f"Job Calling: {self.name}")
        response = self.call(self.url, input, headers, params)
        if response.status_code >= 400:
            if not self.fallback_url:
                raise Exception(
                    f"Job {self.name} returned status code {response.status_code} with body {response.text}"
                )
            response = self.call(self.fallback_url, input, headers, params)
            if response.status_code >= 400:
                raise Exception(
                    f"Job {self.name} returned status code {response.status_code} with body {response.text}"
                )
        return response.text

    async def arun(self, input: Any, headers: dict = {}, params: dict = {}) -> Awaitable[str]:
        logger.debug(f"Job Calling: {self.name}")
        response = await self.acall(self.url, input, headers, params)
        if response.status_code >= 400:
            if not self.fallback_url:
                raise Exception(
                    f"Job {self.name} returned status code {response.status_code} with body {response.text}"
                )
            response = await self.acall(self.fallback_url, input, headers, params)
            if response.status_code >= 400:
                raise Exception(
                    f"Job {self.name} returned status code {response.status_code} with body {response.text}"
                )
        return response.text

    def __str__(self):
        return f"Job {self.name}"

    def __repr__(self):
        return self.__str__()


def bl_job(name: str):
    return BlJob(name)


# Create a singleton instance
bl_start_job = BlJobWrapper()
