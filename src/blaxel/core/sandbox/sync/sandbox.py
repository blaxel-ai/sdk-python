import logging
import uuid
from typing import Any, Dict, List, Union

from ...client.api.compute.create_sandbox import sync as create_sandbox
from ...client.api.compute.delete_sandbox import sync as delete_sandbox
from ...client.api.compute.get_sandbox import sync as get_sandbox
from ...client.api.compute.list_sandboxes import sync as list_sandboxes
from ...client.api.compute.update_sandbox import sync as update_sandbox
from ...client.client import client
from ...client.models import Metadata, Runtime, Sandbox, SandboxSpec
from ...client.types import UNSET
from ..types import (
    SandboxConfiguration,
    SandboxCreateConfiguration,
    SandboxUpdateMetadata,
    SessionWithToken,
)
from .codegen import SyncSandboxCodegen
from .filesystem import SyncSandboxFileSystem
from .network import SyncSandboxNetwork
from .preview import SyncSandboxPreviews
from .process import SyncSandboxProcess
from .session import SyncSandboxSessions

logger = logging.getLogger(__name__)


class SyncSandboxInstance:
    def __init__(
        self,
        sandbox: Union[Sandbox, SandboxConfiguration],
        force_url: str | None = None,
        headers: Dict[str, str] | None = None,
        params: Dict[str, str] | None = None,
    ):
        if isinstance(sandbox, SandboxConfiguration):
            self.config = sandbox
            self.sandbox = sandbox.sandbox
        else:
            self.sandbox = sandbox
            self.config = SandboxConfiguration(
                sandbox=sandbox,
                force_url=force_url,
                headers=headers,
                params=params,
            )
        self.process = SyncSandboxProcess(self.config)
        self.fs = SyncSandboxFileSystem(self.config, self.process)
        self.previews = SyncSandboxPreviews(self.sandbox)
        self.sessions = SyncSandboxSessions(self.config)
        self.network = SyncSandboxNetwork(self.config)
        self.codegen = SyncSandboxCodegen(self.config)

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

    def wait(self, max_wait: int = 60000, interval: int = 1000) -> "SyncSandboxInstance":
        logger.warning(
            "⚠️  Warning: sandbox.wait() is deprecated. You don't need to wait for the sandbox to be deployed anymore."
        )
        return self

    @classmethod
    def create(
        cls,
        sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any], None] = None,
        safe: bool = True,
    ) -> "SyncSandboxInstance":
        default_name = f"sandbox-{uuid.uuid4().hex[:8]}"
        default_image = "blaxel/base-image:latest"
        default_memory = 4096
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
                    or "snapshot_enabled" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                )
            )
        ):
            if sandbox is None:
                sandbox = SandboxCreateConfiguration()
            elif isinstance(sandbox, dict) and not isinstance(sandbox, Sandbox):
                sandbox = SandboxCreateConfiguration.from_dict(sandbox)
            name = sandbox.name or default_name
            image = sandbox.image or default_image
            memory = sandbox.memory or default_memory
            ports = sandbox._normalize_ports() or UNSET
            envs = sandbox._normalize_envs() or UNSET
            volumes = sandbox._normalize_volumes() or UNSET
            ttl = sandbox.ttl
            expires = sandbox.expires
            region = sandbox.region
            lifecycle = sandbox.lifecycle
            sandbox = Sandbox(
                metadata=Metadata(name=name),
                spec=SandboxSpec(
                    runtime=Runtime(
                        image=image, memory=memory, ports=ports, envs=envs, generation="mk3"
                    ),
                    volumes=volumes,
                ),
            )
            if ttl:
                sandbox.spec.runtime.ttl = ttl
            if expires:
                sandbox.spec.runtime.expires = expires.isoformat()
            if region:
                sandbox.spec.region = region
            if lifecycle:
                sandbox.spec.lifecycle = lifecycle
        else:
            if isinstance(sandbox, dict):
                sandbox = Sandbox.from_dict(sandbox)
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
        response = create_sandbox(
            client=client,
            body=sandbox,
        )
        instance = cls(response)
        if safe:
            try:
                instance.fs.ls("/")
            except Exception:
                pass
        return instance

    @classmethod
    def get(cls, sandbox_name: str) -> "SyncSandboxInstance":
        response = get_sandbox(
            sandbox_name,
            client=client,
        )
        return cls(response)

    @classmethod
    def list(cls) -> List["SyncSandboxInstance"]:
        response = list_sandboxes(client=client)
        return [cls(sandbox) for sandbox in response]

    @classmethod
    def delete(cls, sandbox_name: str) -> Sandbox:
        response = delete_sandbox(
            sandbox_name,
            client=client,
        )
        return response

    @classmethod
    def update_metadata(cls, sandbox_name: str, metadata: SandboxUpdateMetadata) -> "SyncSandboxInstance":
        sandbox_instance = cls.get(sandbox_name)
        sandbox = sandbox_instance.sandbox
        updated_sandbox = Sandbox.from_dict(sandbox.to_dict())
        if updated_sandbox.metadata is None:
            updated_sandbox.metadata = Metadata()
        if metadata.labels is not None:
            if updated_sandbox.metadata.labels is None or updated_sandbox.metadata.labels is UNSET:
                updated_sandbox.metadata.labels = {}
            else:
                updated_sandbox.metadata.labels = dict(updated_sandbox.metadata.labels)
            updated_sandbox.metadata.labels.update(metadata.labels)
        if metadata.display_name is not None:
            updated_sandbox.metadata.display_name = metadata.display_name
        response = update_sandbox(
            sandbox_name=sandbox_name,
            client=client,
            body=updated_sandbox,
        )
        return cls(response)

    @classmethod
    def create_if_not_exists(
        cls, sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any]]
    ) -> "SyncSandboxInstance":
        try:
            return cls.create(sandbox)
        except Exception as e:
            if (hasattr(e, "status_code") and e.status_code == 409) or (
                hasattr(e, "code") and e.code in [409, "SANDBOX_ALREADY_EXISTS"]
            ):
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
                sandbox_instance = cls.get(name)
                if sandbox_instance.status == "TERMINATED":
                    return cls.create(sandbox)
                return sandbox_instance
            raise e

    @classmethod
    def from_session(cls, session: Union[SessionWithToken, Dict[str, Any]]) -> "SyncSandboxInstance":
        if isinstance(session, dict):
            session = SessionWithToken.from_dict(session)
        sandbox_name = session.name.split("-")[0] if "-" in session.name else session.name
        sandbox = Sandbox(metadata=Metadata(name=sandbox_name))
        return cls(
            sandbox=sandbox,
            force_url=session.url,
            headers={"X-Blaxel-Preview-Token": session.token},
            params={"bl_preview_token": session.token},
        )


