import logging
import uuid
from typing import Any, Callable, Dict, List, Union

from ...client.api.compute.create_sandbox import asyncio as create_sandbox
from ...client.api.compute.delete_sandbox import asyncio as delete_sandbox
from ...client.api.compute.get_sandbox import asyncio as get_sandbox
from ...client.api.compute.list_sandboxes import asyncio as list_sandboxes
from ...client.api.compute.update_sandbox import asyncio as update_sandbox
from ...client.client import client
from ...client.models import Metadata, Sandbox, SandboxRuntime, SandboxSpec
from ...client.models.error import Error
from ...client.models.sandbox_error import SandboxError
from ...client.types import UNSET
from ..types import (
    SandboxConfiguration,
    SandboxCreateConfiguration,
    SandboxUpdateMetadata,
    SessionWithToken,
)
from .codegen import SandboxCodegen
from .filesystem import SandboxFileSystem
from .network import SandboxNetwork
from .preview import SandboxPreviews
from .process import SandboxProcess
from .session import SandboxSessions


class SandboxAPIError(Exception):
    """Exception raised when sandbox API returns an error."""

    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


logger = logging.getLogger(__name__)


class _AsyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: SandboxInstance.delete("name")
            return self._delete_func
        else:
            # Called on an instance: instance.delete()
            async def instance_delete() -> Sandbox:
                return await self._delete_func(instance.metadata.name)

            return instance_delete


class SandboxInstance:
    delete: "_AsyncDeleteDescriptor"

    def __init__(
        self,
        sandbox: Union[Sandbox, SandboxConfiguration],
        force_url: str | None = None,
        headers: Dict[str, str] | None = None,
        params: Dict[str, str] | None = None,
    ):
        # Handle both Sandbox and SandboxConfiguration inputs
        if isinstance(sandbox, SandboxConfiguration):
            self.config = sandbox
            self.sandbox = sandbox.sandbox
        else:
            # Create SandboxConfiguration with optional parameters
            self.sandbox = sandbox
            self.config = SandboxConfiguration(
                sandbox=sandbox,
                force_url=force_url,
                headers=headers,
                params=params,
            )

        self.process = SandboxProcess(self.config)
        self.fs = SandboxFileSystem(self.config, self.process)
        self.previews = SandboxPreviews(self.sandbox)
        self.sessions = SandboxSessions(self.config)
        self.network = SandboxNetwork(self.config)
        self.codegen = SandboxCodegen(self.config)

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
        default_name = f"sandbox-{uuid.uuid4().hex[:8]}"
        default_image = "blaxel/base-image:latest"
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
                    or "region" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "lifecycle" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "snapshot_enabled"
                    in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "labels" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                )
            )
        ):
            config: SandboxCreateConfiguration
            if sandbox is None:
                config = SandboxCreateConfiguration()
            elif isinstance(sandbox, dict) and not isinstance(sandbox, Sandbox):
                config = SandboxCreateConfiguration.from_dict(sandbox)
            elif isinstance(sandbox, SandboxCreateConfiguration):
                config = sandbox
            else:
                raise ValueError(f"Unexpected sandbox type: {type(sandbox)}")

            # Set defaults if not provided
            name = config.name or default_name
            image = config.image or default_image
            memory = config.memory or default_memory
            ports = config._normalize_ports() or UNSET
            envs = config._normalize_envs() or UNSET
            volumes = config._normalize_volumes() or UNSET
            ttl = config.ttl
            expires = config.expires
            region = config.region
            lifecycle = config.lifecycle
            # snapshot_enabled = sandbox.snapshot_enabled

            # Create full Sandbox object
            sandbox = Sandbox(
                metadata=Metadata(name=name, labels=config.labels),
                spec=SandboxSpec(
                    runtime=SandboxRuntime(
                        image=image,
                        memory=memory,
                        ports=ports,
                        envs=envs,
                    ),
                    volumes=volumes,
                ),
            )

            # Set ttl and expires if provided
            if ttl:
                sandbox.spec.runtime.ttl = ttl
            if expires:
                sandbox.spec.runtime.expires = expires.isoformat()
            if region:
                sandbox.spec.region = region
            if lifecycle:
                sandbox.spec.lifecycle = lifecycle
        else:
            # Handle existing Sandbox object or dict conversion
            if isinstance(sandbox, dict):
                sandbox = Sandbox.from_dict(sandbox)

            # Set defaults for missing fields
            if not sandbox.metadata:
                sandbox.metadata = Metadata(name=default_name)
            if not sandbox.spec:
                sandbox.spec = SandboxSpec(
                    runtime=SandboxRuntime(image=default_image, memory=default_memory)
                )
            if not sandbox.spec.runtime:
                sandbox.spec.runtime = SandboxRuntime(image=default_image, memory=default_memory)

            sandbox.spec.runtime.image = sandbox.spec.runtime.image or default_image
            sandbox.spec.runtime.memory = sandbox.spec.runtime.memory or default_memory

        response = await create_sandbox(
            client=client,
            body=sandbox,
        )

        # Check if response is an error
        if isinstance(response, SandboxError):
            status_code = response.status_code if response.status_code is not UNSET else None
            code = response.code if response.code else None
            message = response.message if response.message else str(response)
            raise SandboxAPIError(message, status_code=status_code, code=code)

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

        # Check if response is an error
        if isinstance(response, Error):
            status_code = response.code if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise SandboxAPIError(message, status_code=status_code, code=response.error)

        if response is None:
            raise SandboxAPIError(f"Sandbox '{sandbox_name}' not found", status_code=404)

        return cls(response)

    @classmethod
    async def list(cls) -> List["SandboxInstance"]:
        response = await list_sandboxes(client=client)
        return [cls(sandbox) for sandbox in response]

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
        if updated_sandbox is None:
            raise ValueError(f"Sandbox {sandbox_name} not found")

        # Merge metadata
        if updated_sandbox.metadata is None:
            updated_sandbox.metadata = Metadata(name=sandbox_name)

        # Update labels if provided
        if metadata.labels is not None:
            # Handle UNSET or None labels
            if updated_sandbox.metadata.labels is None or updated_sandbox.metadata.labels is UNSET:
                updated_sandbox.metadata.labels = {}
            else:
                # If labels exist, convert to dict (MetadataLabels stores in additional_properties)
                if hasattr(updated_sandbox.metadata.labels, "to_dict"):
                    updated_sandbox.metadata.labels = updated_sandbox.metadata.labels.to_dict()
                else:
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
        except SandboxAPIError as e:
            # Check if it's a 409 conflict error (sandbox already exists)
            if e.status_code == 409 or e.code in [409, "SANDBOX_ALREADY_EXISTS"]:
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

                # Get the existing sandbox to check its status
                sandbox_instance = await cls.get(name)

                # If the sandbox is TERMINATED, treat it as not existing
                if sandbox_instance.status == "TERMINATED":
                    # Create a new sandbox - backend will handle cleanup of the terminated one
                    return await cls.create(sandbox)

                # Otherwise return the existing active sandbox
                return sandbox_instance
            raise

    @classmethod
    async def from_session(
        cls, session: Union[SessionWithToken, Dict[str, Any]]
    ) -> "SandboxInstance":
        """Create a sandbox instance from a session with token."""
        if isinstance(session, dict):
            session = SessionWithToken.from_dict(session)

        # Create a minimal sandbox configuration for session-based access
        sandbox_name = session.name.split("-")[0] if "-" in session.name else session.name
        sandbox = Sandbox(metadata=Metadata(name=sandbox_name), spec=SandboxSpec())

        # Use the constructor with force_url, headers, and params
        return cls(
            sandbox=sandbox,
            force_url=session.url,
            headers={"X-Blaxel-Preview-Token": session.token},
            params={"bl_preview_token": session.token},
        )


async def _delete_sandbox_by_name(sandbox_name: str) -> Sandbox:
    """Delete a sandbox by name."""
    response = await delete_sandbox(
        sandbox_name,
        client=client,
    )
    if response is None:
        raise ValueError(f"Sandbox {sandbox_name} not found")
    return response


# Assign the delete descriptor to support both class-level and instance-level calls
SandboxInstance.delete = _AsyncDeleteDescriptor(_delete_sandbox_by_name)
