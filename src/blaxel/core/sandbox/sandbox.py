import logging
import uuid
from typing import Any, Dict, List, Union

from ..client.api.compute.create_sandbox import asyncio as create_sandbox
from ..client.api.compute.delete_sandbox import asyncio as delete_sandbox
from ..client.api.compute.get_sandbox import asyncio as get_sandbox
from ..client.api.compute.list_sandboxes import asyncio as list_sandboxes
from ..client.api.compute.update_sandbox import asyncio as update_sandbox
from ..client.client import client
from ..client.models import Metadata, Runtime, Sandbox, SandboxSpec
from ..client.types import UNSET
from ..common.settings import settings
from .filesystem import SandboxFileSystem
from .network import SandboxNetwork
from .preview import SandboxPreviews
from .process import SandboxProcess
from .session import SandboxSessions
from .types import (
    SandboxConfiguration,
    SandboxCreateConfiguration,
    SandboxUpdateMetadata,
    SessionWithToken,
)

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

    async def wait(self, max_wait: int = 60000, interval: int = 1000) -> "SandboxInstance":
        logger.warning(
            "⚠️  Warning: sandbox.wait() is deprecated. You don't need to wait for the sandbox to be deployed anymore."
        )
        return self

    @classmethod
    async def create(
        cls,
        sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any], None] = None,
        safe: bool = True,
    ) -> "SandboxInstance":
        # Generate default values
        env = settings.env
        default_name = f"sandbox-{uuid.uuid4().hex[:8]}"
        default_image = f"blaxel/{env}-base:latest"
        default_memory = 4096

        # Handle SandboxCreateConfiguration or simple dict with name/image/memory/ports/envs/volumes keys
        if (
            sandbox is None
            or isinstance(sandbox, SandboxCreateConfiguration | dict)
            and (
                not isinstance(sandbox, Sandbox)
                and (
                    sandbox is None
                    or "name" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "image" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "memory" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "ports" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "envs" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "volumes" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "ttl" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "expires" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                )
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
            ports = sandbox._normalize_ports() or UNSET
            envs = sandbox._normalize_envs() or UNSET
            volumes = sandbox._normalize_volumes() or UNSET
            ttl = sandbox.ttl
            expires = sandbox.expires

            # Create full Sandbox object
            sandbox = Sandbox(
                metadata=Metadata(name=name),
                spec=SandboxSpec(
                    runtime=Runtime(
                        image=image, memory=memory, ports=ports, envs=envs, generation="mk3"
                    ),
                    volumes=volumes,
                ),
            )

            # Set ttl and expires if provided
            if ttl:
                sandbox.spec.runtime.ttl = ttl
            if expires:
                sandbox.spec.runtime.expires = expires.isoformat()
        else:
            # Handle existing Sandbox object or dict conversion
            if isinstance(sandbox, dict):
                sandbox = Sandbox.from_dict(sandbox)

            # Set defaults for missing fields
            if not sandbox.metadata:
                sandbox.metadata = Metadata(name=default_name)
            if not sandbox.spec:
                sandbox.spec = SandboxSpec(
                    runtime=Runtime(image=default_image, memory=default_memory)
                )
            if not sandbox.spec.runtime:
                sandbox.spec.runtime = Runtime(image=default_image, memory=default_memory)

            sandbox.spec.runtime.image = sandbox.spec.runtime.image or default_image
            sandbox.spec.runtime.memory = sandbox.spec.runtime.memory or default_memory
            sandbox.spec.runtime.generation = sandbox.spec.runtime.generation or "mk3"

        response = await create_sandbox(
            client=client,
            body=sandbox,
        )
        instance = cls(response)
        # TODO remove this part once we have a better way to handle this
        if safe:
            try:
                await instance.fs.ls("/")
            except Exception:
                pass
        return instance

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
    async def update_metadata(
        cls, sandbox_name: str, metadata: SandboxUpdateMetadata
    ) -> "SandboxInstance":
        """Update sandbox metadata by merging new metadata with existing metadata.

        Args:
            sandbox_name: The name of the sandbox to update
            metadata: The metadata fields to update (labels and/or display_name)

        Returns:
            A new SandboxInstance with updated metadata
        """
        # Get the existing sandbox
        sandbox_instance = await cls.get(sandbox_name)
        sandbox = sandbox_instance.sandbox

        # Prepare the updated sandbox object
        updated_sandbox = Sandbox.from_dict(sandbox.to_dict())

        # Merge metadata
        if updated_sandbox.metadata is None:
            updated_sandbox.metadata = Metadata()

        # Update labels if provided
        if metadata.labels is not None:
            # Handle UNSET or None labels
            if updated_sandbox.metadata.labels is None or updated_sandbox.metadata.labels is UNSET:
                updated_sandbox.metadata.labels = {}
            else:
                # If labels exist, ensure it's a dict
                updated_sandbox.metadata.labels = dict(updated_sandbox.metadata.labels)
            updated_sandbox.metadata.labels.update(metadata.labels)

        # Update display_name if provided
        if metadata.display_name is not None:
            updated_sandbox.metadata.display_name = metadata.display_name

        # Call the update API
        response = await update_sandbox(
            sandbox_name=sandbox_name,
            client=client,
            body=updated_sandbox,
        )

        # Return new instance with updated sandbox
        return cls(response)

    @classmethod
    async def create_if_not_exists(
        cls, sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any]]
    ) -> "SandboxInstance":
        """Create a sandbox if it doesn't exist, otherwise return existing."""
        try:
            return await cls.create(sandbox)
        except Exception as e:
            # Check if it's a 409 conflict error (sandbox already exists)
            if (hasattr(e, "status_code") and e.status_code == 409) or (
                hasattr(e, "code") and e.code in [409, "SANDBOX_ALREADY_EXISTS"]
            ):
                # Extract name from different configuration types
                if isinstance(sandbox, SandboxCreateConfiguration):
                    name = sandbox.name
                elif isinstance(sandbox, dict):
                    if "name" in sandbox:
                        name = sandbox["name"]
                    elif "metadata" in sandbox and isinstance(sandbox["metadata"], dict):
                        name = sandbox["metadata"].get("name")
                    else:
                        name = None
                elif isinstance(sandbox, Sandbox):
                    name = sandbox.metadata.name if sandbox.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Sandbox name is required")

                sandbox_instance = await cls.get(name)
                return sandbox_instance
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
