from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union

from attrs import define as _attrs_define

from ..client.models import Port, Sandbox, VolumeAttachment
from ..client.types import UNSET
from .client.models.process_request import ProcessRequest
from .client.models.process_response import ProcessResponse


class SessionCreateOptions:
    def __init__(
        self,
        expires_at: Optional[datetime] = None,
        response_headers: Optional[Dict[str, str]] = None,
        request_headers: Optional[Dict[str, str]] = None,
    ):
        self.expires_at = expires_at
        self.response_headers = response_headers or {}
        self.request_headers = request_headers or {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionCreateOptions":
        expires_at = None
        if "expires_at" in data and data["expires_at"]:
            if isinstance(data["expires_at"], str):
                expires_at = datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
            elif isinstance(data["expires_at"], datetime):
                expires_at = data["expires_at"]

        return cls(
            expires_at=expires_at,
            response_headers=data.get("response_headers"),
            request_headers=data.get("request_headers"),
        )


class SessionWithToken:
    def __init__(self, name: str, url: str, token: str, expires_at: datetime):
        self.name = name
        self.url = url
        self.token = token
        self.expires_at = expires_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionWithToken":
        expires_at = data["expires_at"]
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))

        return cls(
            name=data["name"],
            url=data["url"],
            token=data["token"],
            expires_at=expires_at,
        )


class VolumeBinding:
    """Volume binding configuration for sandbox."""

    def __init__(self, name: str, mount_path: str, read_only: Optional[bool] = False):
        self.name = name
        self.mount_path = mount_path
        self.read_only = read_only or False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VolumeBinding":
        return cls(
            name=data["name"],
            mount_path=data["mount_path"],
            read_only=data.get("read_only", False),
        )


class SandboxConfiguration:
    def __init__(
        self,
        sandbox: Sandbox,
        force_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
    ):
        self.sandbox = sandbox
        self.force_url = force_url
        self.headers = headers or {}
        self.params = params or {}

    @property
    def metadata(self):
        return self.sandbox.metadata

    @property
    def status(self):
        return self.sandbox.status

    @property
    def spec(self):
        return self.sandbox.spec


class WatchEvent:
    def __init__(self, op: str, path: str, name: str, content: Optional[str] = None):
        self.op = op
        self.path = path
        self.name = name
        self.content = content


class SandboxFilesystemFile:
    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SandboxFilesystemFile":
        return cls(data["path"], data["content"])


class CopyResponse:
    def __init__(self, message: str, source: str, destination: str):
        self.message = message
        self.source = source
        self.destination = destination


class SandboxUpdateMetadata:
    """Configuration for updating sandbox metadata."""

    def __init__(
        self,
        labels: Optional[Dict[str, str]] = None,
        display_name: Optional[str] = None,
    ):
        self.labels = labels
        self.display_name = display_name


class SandboxCreateConfiguration:
    """Simplified configuration for creating sandboxes with default values."""

    def __init__(
        self,
        name: Optional[str] = None,
        image: Optional[str] = None,
        memory: Optional[int] = None,
        ports: Optional[Union[List[Port], List[Dict[str, Any]]]] = None,
        envs: Optional[List[Dict[str, str]]] = None,
        volumes: Optional[Union[List[VolumeBinding], List[VolumeAttachment], List[Dict[str, Any]]]] = None,
        ttl: Optional[str] = None,
        expires: Optional[datetime] = None,
    ):
        self.name = name
        self.image = image
        self.memory = memory
        self.ports = ports
        self.envs = envs
        self.volumes = volumes
        self.ttl = ttl
        self.expires = expires

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SandboxCreateConfiguration":
        expires = data.get("expires")
        if expires and isinstance(expires, str):
            expires = datetime.fromisoformat(expires.replace("Z", "+00:00"))

        return cls(
            name=data.get("name"),
            image=data.get("image"),
            memory=data.get("memory"),
            ports=data.get("ports"),
            envs=data.get("envs"),
            volumes=data.get("volumes"),
            ttl=data.get("ttl"),
            expires=expires,
        )

    def _normalize_ports(self) -> Optional[List[Port]]:
        """Convert ports to Port objects with default protocol HTTP if not specified."""
        if not self.ports:
            return None

        port_objects = []
        for port in self.ports:
            if isinstance(port, Port):
                # If it's already a Port object, ensure protocol defaults to HTTP
                if port.protocol is UNSET or not port.protocol:
                    port.protocol = "HTTP"
                port_objects.append(port)
            elif isinstance(port, dict):
                # Convert dict to Port object with HTTP as default protocol
                port_dict = port.copy()
                if "protocol" not in port_dict or not port_dict["protocol"]:
                    port_dict["protocol"] = "HTTP"
                port_objects.append(Port.from_dict(port_dict))
            else:
                raise ValueError(f"Invalid port type: {type(port)}. Expected Port object or dict.")

        return port_objects

    def _normalize_envs(self) -> Optional[List[Dict[str, str]]]:
        """Convert envs to list of dicts with name and value keys."""
        if not self.envs:
            return None

        env_objects = []
        for env in self.envs:
            if isinstance(env, dict):
                # Validate that the dict has the required keys
                if "name" not in env or "value" not in env:
                    raise ValueError(
                        f"Environment variable dict must have 'name' and 'value' keys: {env}"
                    )
                env_objects.append({"name": env["name"], "value": env["value"]})
            else:
                raise ValueError(
                    f"Invalid env type: {type(env)}. Expected dict with 'name' and 'value' keys."
                )

        return env_objects

    def _normalize_volumes(self) -> Optional[List[VolumeAttachment]]:
        """Convert volumes to VolumeAttachment objects."""
        if not self.volumes:
            return None

        volume_objects = []
        for volume in self.volumes:
            if isinstance(volume, VolumeAttachment):
                volume_objects.append(volume)
            elif isinstance(volume, VolumeBinding):
                # Convert VolumeBinding to VolumeAttachment format
                volume_attachment = VolumeAttachment(
                    name=volume.name,
                    mount_path=volume.mount_path,
                    read_only=volume.read_only,
                )
                volume_objects.append(volume_attachment)
            elif isinstance(volume, dict):
                # Validate that the dict has the required keys
                if "name" not in volume or "mount_path" not in volume:
                    raise ValueError(
                        f"Volume binding dict must have 'name' and 'mount_path' keys: {volume}"
                    )
                if not isinstance(volume["name"], str) or not isinstance(volume["mount_path"], str):
                    raise ValueError(
                        f"Volume binding 'name' and 'mount_path' must be strings: {volume}"
                    )

                # Convert dict to VolumeAttachment object
                volume_attachment = VolumeAttachment(
                    name=volume["name"],
                    mount_path=volume["mount_path"],
                    read_only=volume.get("read_only", False),
                )
                volume_objects.append(volume_attachment)
            else:
                raise ValueError(
                    f"Invalid volume type: {type(volume)}. Expected VolumeAttachment, VolumeBinding, or dict with 'name' and 'mount_path' keys."
                )

        return volume_objects


@_attrs_define
class ProcessRequestWithLog(ProcessRequest):
    on_log: Callable[[str], None] = None


class ProcessResponseWithLog:
    """A process response with additional close functionality for stream management."""

    def __init__(self, process_response: ProcessResponse, close_func: Callable[[], None]):
        self._process_response = process_response
        self._close_func = close_func

    def close(self) -> None:
        """Close the log stream without terminating the process."""
        self._close_func()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the underlying ProcessResponse."""
        return getattr(self._process_response, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Handle setting attributes, preserving special attributes."""
        if name.startswith("_") or name == "close":
            super().__setattr__(name, value)
        else:
            setattr(self._process_response, name, value)
