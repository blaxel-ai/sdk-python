import uuid
from typing import Callable, Dict, List, Union

from ..client.api.volumes.create_volume import asyncio as create_volume
from ..client.api.volumes.create_volume import sync as create_volume_sync
from ..client.api.volumes.delete_volume import asyncio as delete_volume
from ..client.api.volumes.delete_volume import sync as delete_volume_sync
from ..client.api.volumes.get_volume import asyncio as get_volume
from ..client.api.volumes.get_volume import sync as get_volume_sync
from ..client.api.volumes.list_volumes import asyncio as list_volumes
from ..client.api.volumes.list_volumes import sync as list_volumes_sync
from ..client.client import client
from ..client.models import Metadata, Volume, VolumeSpec
from ..client.models.error import Error
from ..client.types import UNSET


class VolumeAPIError(Exception):
    """Exception raised when volume API returns an error."""

    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class _AsyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: VolumeInstance.delete("name")
            return self._delete_func
        else:
            # Called on an instance: instance.delete()
            async def instance_delete() -> Volume:
                return await self._delete_func(instance.metadata.name or "")

            return instance_delete


class _SyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality (sync)."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: SyncVolumeInstance.delete("name")
            return self._delete_func
        else:
            # Called on an instance: instance.delete()
            def instance_delete() -> Volume:
                return self._delete_func(instance.metadata.name or "")

            return instance_delete


class VolumeCreateConfiguration:
    """Simplified configuration for creating volumes with default values."""

    def __init__(
        self,
        name: str | None = None,
        display_name: str | None = None,
        labels: Dict[str, str] | None = None,
        size: int | None = None,  # Size in MB
        region: str | None = None,  # AWS region
        template: str | None = None,  # Template
    ):
        self.name = name
        self.display_name = display_name
        self.labels = labels
        self.size = size
        self.region = region
        self.template = template

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "VolumeCreateConfiguration":
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            labels=data.get("labels"),
            size=data.get("size"),
            region=data.get("region"),
            template=data.get("template"),
        )


class VolumeInstance:
    def __init__(self, volume: Volume):
        self.volume = volume

    @property
    def metadata(self):
        return self.volume.metadata

    @property
    def spec(self):
        return self.volume.spec

    @property
    def status(self):
        return self.volume.status

    @property
    def name(self):
        return self.volume.metadata.name if self.volume.metadata else None

    @property
    def display_name(self):
        return self.volume.metadata.display_name if self.volume.metadata else None

    @property
    def size(self):
        return self.volume.spec.size if self.volume.spec else None

    @property
    def region(self):
        return self.volume.spec.region if self.volume.spec else None

    @property
    def template(self):
        return self.volume.spec.template if self.volume.spec else None

    @classmethod
    async def create(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "VolumeInstance":
        # Generate default values
        default_name = f"volume-{uuid.uuid4().hex[:8]}"
        default_size = 1024  # 1GB in MB

        # Handle different configuration types
        if isinstance(config, Volume):
            volume = config
        elif isinstance(config, VolumeCreateConfiguration):
            volume = Volume(
                metadata=Metadata(
                    name=config.name or default_name,
                    display_name=config.display_name or config.name or default_name,
                    labels=config.labels,
                ),
                spec=VolumeSpec(
                    size=config.size or default_size,
                    region=config.region or UNSET,
                    template=config.template or UNSET,
                ),
            )
        elif isinstance(config, dict):
            volume_config = VolumeCreateConfiguration.from_dict(config)
            volume = Volume(
                metadata=Metadata(
                    name=volume_config.name or default_name,
                    display_name=volume_config.display_name or volume_config.name or default_name,
                    labels=volume_config.labels,
                ),
                spec=VolumeSpec(
                    size=volume_config.size or default_size,
                    region=volume_config.region or UNSET,
                    template=volume_config.template or UNSET,
                ),
            )
        else:
            raise ValueError(
                f"Invalid config type: {type(config)}. Expected VolumeCreateConfiguration, Volume, or dict."
            )

        # Ensure required fields have defaults
        if not volume.metadata:
            volume.metadata = Metadata(name=default_name)
        if not volume.metadata.name:
            volume.metadata.name = default_name
        if not volume.spec:
            volume.spec = VolumeSpec(size=default_size)
        if not volume.spec.size:
            volume.spec.size = default_size

        response = await create_volume(client=client, body=volume)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    async def get(cls, volume_name: str) -> "VolumeInstance":
        response = await get_volume(volume_name=volume_name, client=client)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    async def list(cls) -> list["VolumeInstance"]:
        response = await list_volumes(client=client)
        return [cls(volume) for volume in response or []]

    @classmethod
    async def create_if_not_exists(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "VolumeInstance":
        """Create a volume if it doesn't exist, otherwise return existing."""
        try:
            return await cls.create(config)
        except VolumeAPIError as e:
            # Check if it's a 409 conflict error (volume already exists)
            if e.status_code == 409 or e.code in ["409", "VOLUME_ALREADY_EXISTS"]:
                # Extract name from different configuration types
                if isinstance(config, VolumeCreateConfiguration):
                    name = config.name
                elif isinstance(config, dict):
                    name = config.get("name")
                elif isinstance(config, Volume):
                    name = config.metadata.name if config.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Volume name is required")

                volume_instance = await cls.get(name)
                return volume_instance
            raise


class SyncVolumeInstance:
    """Synchronous volume instance for managing persistent storage."""

    def __init__(self, volume: Volume):
        self.volume = volume

    @property
    def metadata(self):
        return self.volume.metadata

    @property
    def spec(self):
        return self.volume.spec

    @property
    def status(self):
        return self.volume.status

    @property
    def name(self):
        return self.volume.metadata.name if self.volume.metadata else None

    @property
    def display_name(self):
        return self.volume.metadata.display_name if self.volume.metadata else None

    @property
    def size(self):
        return self.volume.spec.size if self.volume.spec else None

    @property
    def region(self):
        return self.volume.spec.region if self.volume.spec else None

    @property
    def template(self):
        return self.volume.spec.template if self.volume.spec else None

    @classmethod
    def create(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "SyncVolumeInstance":
        """Create a new volume synchronously."""
        # Generate default values
        default_name = f"volume-{uuid.uuid4().hex[:8]}"
        default_size = 1024  # 1GB in MB

        # Handle different configuration types
        if isinstance(config, Volume):
            volume = config
        elif isinstance(config, VolumeCreateConfiguration):
            volume = Volume(
                metadata=Metadata(
                    name=config.name or default_name,
                    display_name=config.display_name or config.name or default_name,
                    labels=config.labels,
                ),
                spec=VolumeSpec(
                    size=config.size or default_size,
                    region=config.region or UNSET,
                    template=config.template or UNSET,
                ),
            )
        elif isinstance(config, dict):
            volume_config = VolumeCreateConfiguration.from_dict(config)
            volume = Volume(
                metadata=Metadata(
                    name=volume_config.name or default_name,
                    display_name=volume_config.display_name or volume_config.name or default_name,
                    labels=volume_config.labels,
                ),
                spec=VolumeSpec(
                    size=volume_config.size or default_size,
                    region=volume_config.region or UNSET,
                    template=volume_config.template or UNSET,
                ),
            )
        else:
            raise ValueError(
                f"Invalid config type: {type(config)}. Expected VolumeCreateConfiguration, Volume, or dict."
            )

        # Ensure required fields have defaults
        if not volume.metadata:
            volume.metadata = Metadata(name=default_name)
        if not volume.metadata.name:
            volume.metadata.name = default_name
        if not volume.spec:
            volume.spec = VolumeSpec(size=default_size)
        if not volume.spec.size:
            volume.spec.size = default_size

        response = create_volume_sync(client=client, body=volume)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    def get(cls, volume_name: str) -> "SyncVolumeInstance":
        """Get a volume by name synchronously."""
        response = get_volume_sync(volume_name=volume_name, client=client)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    def list(cls) -> List["SyncVolumeInstance"]:
        """List all volumes synchronously."""
        response = list_volumes_sync(client=client)
        return [cls(volume) for volume in response or []]

    @classmethod
    def create_if_not_exists(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "SyncVolumeInstance":
        """Create a volume if it doesn't exist, otherwise return existing."""
        try:
            return cls.create(config)
        except VolumeAPIError as e:
            # Check if it's a 409 conflict error (volume already exists)
            if e.status_code == 409 or e.code in ["409", "VOLUME_ALREADY_EXISTS"]:
                # Extract name from different configuration types
                if isinstance(config, VolumeCreateConfiguration):
                    name = config.name
                elif isinstance(config, dict):
                    name = config.get("name")
                elif isinstance(config, Volume):
                    name = config.metadata.name if config.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Volume name is required")

                volume_instance = cls.get(name)
                return volume_instance
            raise


async def _delete_volume_by_name(volume_name: str) -> Volume:
    """Delete a volume by name (async)."""
    response = await delete_volume(volume_name=volume_name, client=client)
    return response


def _delete_volume_by_name_sync(volume_name: str) -> Volume:
    """Delete a volume by name (sync)."""
    response = delete_volume_sync(volume_name=volume_name, client=client)
    return response


# Assign the delete descriptors to support both class-level and instance-level calls
VolumeInstance.delete = _AsyncDeleteDescriptor(_delete_volume_by_name)
SyncVolumeInstance.delete = _SyncDeleteDescriptor(_delete_volume_by_name_sync)
