import asyncio
import logging
import time
import uuid
from typing import Any, Dict, List, Union

from ..client.api.compute.create_sandbox import asyncio as create_sandbox
from ..client.api.compute.delete_sandbox import asyncio as delete_sandbox
from ..client.api.compute.get_sandbox import asyncio as get_sandbox
from ..client.api.compute.list_sandboxes import asyncio as list_sandboxes
from ..client.client import client
from ..client.models import Metadata, Runtime, Sandbox, SandboxSpec
from .filesystem import SandboxFileSystem
from .network import SandboxNetwork
from .preview import SandboxPreviews
from .process import SandboxProcess
from .session import SandboxSessions
from .types import SandboxConfiguration, SandboxCreateConfiguration, SessionWithToken

logger = logging.getLogger(__name__)


class SandboxInstance:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox
        self.config = SandboxConfiguration(sandbox)
        self.fs = SandboxFileSystem(self.config)
        self.process = SandboxProcess(self.config)
        self.previews = SandboxPreviews(sandbox)
        self.sessions = SandboxSessions(self.config)
        self.network = SandboxNetwork(self.config)

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
                self.config = SandboxConfiguration(self.sandbox)
            except Exception as e:
                logger.error("Could not retrieve sandbox", exc_info=e)

            if self.sandbox.status == "FAILED":
                raise Exception("Sandbox failed to deploy")

            if (time.time() * 1000) - start_time > max_wait:
                raise Exception("Sandbox did not deploy in time")

    @classmethod
    async def create(
        cls, sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any], None] = None
    ) -> "SandboxInstance":
        # Generate default values
        default_name = f"sandbox-{uuid.uuid4().hex[:8]}"
        default_image = "blaxel/prod-base:latest"
        default_memory = 4096

        # Handle SandboxCreateConfiguration or simple dict with name/image/memory keys
        if sandbox is None or isinstance(sandbox, (SandboxCreateConfiguration, dict)) and (
            not isinstance(sandbox, Sandbox) and (
                sandbox is None or
                'name' in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__) or
                'image' in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__) or
                'memory' in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
            )
        ):
            if sandbox is None:
                sandbox = SandboxCreateConfiguration()
            elif isinstance(sandbox, dict) and not isinstance(sandbox, Sandbox):
                sandbox = SandboxCreateConfiguration.from_dict(sandbox)

            # Set defaults if not provided
            name = sandbox.name or default_name
            image = sandbox.image or default_image
            memory = sandbox.memory or default_memory

            # Create full Sandbox object
            sandbox = Sandbox(
                metadata=Metadata(name=name),
                spec=SandboxSpec(runtime=Runtime(image=image, memory=memory, generation="mk3"))
            )
        else:
            # Handle existing Sandbox object or dict conversion
            if isinstance(sandbox, dict):
                sandbox = Sandbox.from_dict(sandbox)

            # Set defaults for missing fields
            if not sandbox.metadata:
                sandbox.metadata = Metadata(name=uuid.uuid4().hex.replace('-', ''))
            if not sandbox.spec:
                sandbox.spec = SandboxSpec(runtime=Runtime(image=default_image))
            if not sandbox.spec.runtime:
                sandbox.spec.runtime = Runtime(image=default_image, memory=default_memory)

            sandbox.spec.runtime.image = sandbox.spec.runtime.image or default_image
            sandbox.spec.runtime.memory = sandbox.spec.runtime.memory or default_memory
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

    @classmethod
    async def create_if_not_exists(
        cls, sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any]]
    ) -> "SandboxInstance":
        """Create a sandbox if it doesn't exist, otherwise return existing."""
        try:
            # Extract name from different configuration types
            if isinstance(sandbox, SandboxCreateConfiguration):
                name = sandbox.name
            elif isinstance(sandbox, dict):
                if 'name' in sandbox:
                    name = sandbox['name']
                elif 'metadata' in sandbox and isinstance(sandbox['metadata'], dict):
                    name = sandbox['metadata'].get('name')
                else:
                    # If no name provided, we can't check if it exists, so create new
                    return await cls.create(sandbox)
            elif isinstance(sandbox, Sandbox):
                name = sandbox.metadata.name if sandbox.metadata else None
            else:
                name = None

            if not name:
                raise ValueError("Sandbox name is required")

            sandbox_instance = await cls.get(name)
            return sandbox_instance
        except Exception as e:
            # Check if it's a 404 error (sandbox not found)
            if hasattr(e, "status_code") and e.status_code == 404:
                return await cls.create(sandbox)
            raise e

    @classmethod
    async def from_session(
        cls, session: Union[SessionWithToken, Dict[str, Any]]
    ) -> "SandboxInstance":
        """Create a sandbox instance from a session with token."""
        if isinstance(session, dict):
            session = SessionWithToken.from_dict(session)

        # Create a minimal sandbox configuration for session-based access
        sandbox_name = session.name.split("-")[0] if "-" in session.name else session.name
        sandbox = Sandbox(metadata=Metadata(name=sandbox_name))
        config = SandboxConfiguration(
            sandbox=sandbox,
            force_url=session.url,
            headers={"X-Blaxel-Preview-Token": session.token},
            params={"bl_preview_token": session.token},
        )

        instance = cls.__new__(cls)
        instance.sandbox = sandbox
        instance.config = config
        instance.fs = SandboxFileSystem(config)
        instance.process = SandboxProcess(config)
        instance.previews = SandboxPreviews(sandbox)
        instance.sessions = SandboxSessions(config)
        instance.network = SandboxNetwork(config)

        return instance
