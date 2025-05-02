import asyncio
import logging
import time
from typing import List

from ..client.api.compute.create_sandbox import asyncio as create_sandbox
from ..client.api.compute.delete_sandbox import asyncio as delete_sandbox
from ..client.api.compute.get_sandbox import asyncio as get_sandbox
from ..client.api.compute.list_sandboxes import asyncio as list_sandboxes
from ..client.client import client
from ..client.models import Sandbox
from .filesystem import SandboxFileSystem
from .process import SandboxProcess

logger = logging.getLogger(__name__)

class SandboxInstance:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox
        self.fs = SandboxFileSystem(sandbox)
        self.process = SandboxProcess(sandbox)

    @property
    def metadata(self):
        return self.sandbox.metadata

    @property
    def status(self):
        return self.sandbox.status

    @property
    def events(self):
        return self.sandbox.events

    @property
    def spec(self):
        return self.sandbox.spec

    async def wait(self, max_wait: int = 60000, interval: int = 1000) -> None:
        start_time = time.time() * 1000  # Convert to milliseconds
        while self.sandbox.status != "DEPLOYED":
            await asyncio.sleep(interval / 1000)  # Convert to seconds
            try:
                response = await get_sandbox(
                    self.sandbox.metadata.name,
                    client=client,
                )
                logger.info(f"Waiting for sandbox to be deployed, status: {response.status}")
                self.sandbox = response
            except Exception as e:
                logger.error("Could not retrieve sandbox", exc_info=e)

            if self.sandbox.status == "FAILED":
                raise Exception("Sandbox failed to deploy")

            if (time.time() * 1000) - start_time > max_wait:
                raise Exception("Sandbox did not deploy in time")

    @classmethod
    async def create(cls, sandbox: Sandbox) -> "SandboxInstance":
        if not sandbox.spec:
            raise Exception("Sandbox spec is required")
        if not sandbox.spec.runtime:
            raise Exception("Sandbox runtime is required")
        sandbox.spec.runtime.generation = sandbox.spec.runtime.generation or "mk3"

        response = await create_sandbox(
            client=client,
            body=sandbox,
        )
        return cls(response)

    @classmethod
    async def get(cls, sandbox_name: str) -> "SandboxInstance":
        response = await get_sandbox(
            sandbox_name,
            client=client,
        )
        return cls(response)

    @classmethod
    async def list(cls) -> List["SandboxInstance"]:
        response = await list_sandboxes()
        return [cls(sandbox) for sandbox in response]

    @classmethod
    async def delete(cls, sandbox_name: str) -> Sandbox:
        response = await delete_sandbox(
            sandbox_name,
            client=client,
        )
        return response
