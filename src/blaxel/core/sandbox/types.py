from datetime import datetime
from typing import Any, Dict, Optional

from ..client.models import Sandbox


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


class SandboxCreateConfiguration:
    """Simplified configuration for creating sandboxes with default values."""
    def __init__(
        self,
        name: Optional[str] = None,
        image: Optional[str] = None,
        memory: Optional[int] = None,
    ):
        self.name = name
        self.image = image
        self.memory = memory

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SandboxCreateConfiguration":
        return cls(
            name=data.get("name"),
            image=data.get("image"),
            memory=data.get("memory"),
        )
