"""Workspace secrets.

Secrets are write-only: once set, only ``name``, ``created_at`` and ``updated_at``
can be read back. Every ``set`` stores a new immutable version and the latest one is
what the proxy resolves for ``{{SECRET:name}}`` references in a sandbox's routing.
"""

from ..client.api.secrets.delete_secret import asyncio as delete_secret
from ..client.api.secrets.delete_secret import sync as delete_secret_sync
from ..client.api.secrets.list_secrets import asyncio as list_secrets
from ..client.api.secrets.list_secrets import sync as list_secrets_sync
from ..client.api.secrets.upsert_secret import asyncio as upsert_secret
from ..client.api.secrets.upsert_secret import sync as upsert_secret_sync
from ..client.client import client
from ..client.models import Secret
from ..client.types import UNSET
from ..errors import _APIError


class SecretAPIError(_APIError):
    """Exception raised when the secrets API returns an error."""


def _checked(response, action: str):
    if response is None:
        raise SecretAPIError(f"Failed to {action} secret")
    return response


class SecretInstance:
    """Metadata of a workspace secret. The value itself is never readable."""

    def __init__(self, secret: Secret):
        self.secret = secret

    @property
    def name(self) -> str:
        return self.secret.name

    @property
    def created_at(self) -> str | None:
        return None if self.secret.created_at is UNSET else self.secret.created_at

    @property
    def updated_at(self) -> str | None:
        return None if self.secret.updated_at is UNSET else self.secret.updated_at

    @classmethod
    async def set(cls, name: str, value: str) -> "SecretInstance":
        """Create the secret, or store a new version if it already exists."""
        response = await upsert_secret(client=client, body=Secret(name=name, value=value))
        return cls(_checked(response, "set"))

    @classmethod
    async def list(cls) -> list["SecretInstance"]:
        response = await list_secrets(client=client)
        return [cls(secret) for secret in _checked(response, "list")]

    @classmethod
    async def delete(cls, name: str) -> Secret:
        """Delete the secret and all of its versions."""
        response = await delete_secret(secret_name=name, client=client)
        return _checked(response, "delete")


class SyncSecretInstance(SecretInstance):
    """Synchronous version of :class:`SecretInstance`."""

    @classmethod
    def set(cls, name: str, value: str) -> "SyncSecretInstance":
        response = upsert_secret_sync(client=client, body=Secret(name=name, value=value))
        return cls(_checked(response, "set"))

    @classmethod
    def list(cls) -> list["SyncSecretInstance"]:
        response = list_secrets_sync(client=client)
        return [cls(secret) for secret in _checked(response, "list")]

    @classmethod
    def delete(cls, name: str) -> Secret:
        response = delete_secret_sync(secret_name=name, client=client)
        return _checked(response, "delete")
