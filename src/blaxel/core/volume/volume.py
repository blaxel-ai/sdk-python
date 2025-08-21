import uuid
from typing import Dict, Optional, Union

from ..client.api.volumes.create_volume import asyncio as create_volume
from ..client.api.volumes.delete_volume import asyncio as delete_volume
from ..client.api.volumes.get_volume import asyncio as get_volume
from ..client.api.volumes.list_volumes import asyncio as list_volumes
from ..client.client import client
from ..client.models import Metadata, Volume, VolumeSpec
from ..client.types import UNSET


class VolumeCreateConfiguration:
    """Simplified configuration for creating volumes with default values."""

    def __init__(
        self,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        size: Optional[int] = None,  # Size in MB
        region: Optional[str] = None,  # AWS region
    ):
        self.name = name
        self.display_name = display_name
        self.size = size
        self.region = region

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "VolumeCreateConfiguration":
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            size=data.get("size"),
            region=data.get("region"),
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
                ),
                spec=VolumeSpec(
                    size=config.size or default_size,
                    region=config.region or UNSET,
                ),
            )
        elif isinstance(config, dict):
            volume_config = VolumeCreateConfiguration.from_dict(config)
            volume = Volume(
                metadata=Metadata(
                    name=volume_config.name or default_name,
                    display_name=volume_config.display_name or volume_config.name or default_name,
                ),
                spec=VolumeSpec(
                    size=volume_config.size or default_size,
                    region=volume_config.region or UNSET,
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
        return cls(response)

    @classmethod
    async def get(cls, volume_name: str) -> "VolumeInstance":
        response = await get_volume(volume_name=volume_name, client=client)
        return cls(response)

    @classmethod
    async def list(cls) -> list["VolumeInstance"]:
        response = await list_volumes(client=client)
        return [cls(volume) for volume in response or []]

    @classmethod
    async def delete(cls, volume_name: str) -> Volume:
        response = await delete_volume(volume_name=volume_name, client=client)
        return response

    @classmethod
    async def create_if_not_exists(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "VolumeInstance":
        """Create a volume if it doesn't exist, otherwise return existing."""
        try:
            return await cls.create(config)
        except Exception as e:
            # Check if it's a 409 conflict error (volume already exists)
            if (hasattr(e, "status_code") and e.status_code == 409) or (
                hasattr(e, "code") and e.code in [409, "VOLUME_ALREADY_EXISTS"]
            ):
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
            raise e
