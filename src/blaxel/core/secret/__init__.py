"""Secret module for write-only workspace secrets."""

from .secret import SecretAPIError, SecretInstance, SyncSecretInstance

__all__ = ["SecretInstance", "SyncSecretInstance", "SecretAPIError"]
