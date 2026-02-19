import asyncio
import time
import uuid
import warnings
from typing import Callable, Dict, List, Union

from ..client.api.drives.create_drive import asyncio as create_drive
from ..client.api.drives.create_drive import sync as create_drive_sync
from ..client.api.drives.delete_drive import asyncio as delete_drive
from ..client.api.drives.delete_drive import sync as delete_drive_sync
from ..client.api.drives.get_drive import asyncio as get_drive
from ..client.api.drives.get_drive import sync as get_drive_sync
from ..client.api.drives.list_drives import asyncio as list_drives
from ..client.api.drives.list_drives import sync as list_drives_sync
from ..client.api.drives.update_drive import asyncio as update_drive
from ..client.api.drives.update_drive import sync as update_drive_sync
from ..client.client import client
from ..client.models import Drive, DriveSpec, Metadata
from ..client.models.error import Error
from ..client.types import UNSET
from ..common.settings import settings


class DriveAPIError(Exception):
    """Exception raised when drive API returns an error."""

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
            # Called on the class: DriveInstance.delete("name")
            return self._delete_func
        else:
            # Called on an instance: instance.delete()
            async def instance_delete() -> Drive:
                return await self._delete_func(instance.metadata.name or "")

            return instance_delete


class _SyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality (sync)."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: SyncDriveInstance.delete("name")
            return self._delete_func
        else:
            # Called on an instance: instance.delete()
            def instance_delete() -> Drive:
                return self._delete_func(instance.metadata.name or "")

            return instance_delete


class _AsyncUpdateDescriptor:
    """Descriptor that provides both class-level and instance-level update functionality."""

    def __init__(self, update_func: Callable):
        self._update_func = update_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: DriveInstance.update("name", updates)
            return self._update_func
        else:
            # Called on an instance: instance.update(updates)
            async def instance_update(
                updates: Union["DriveCreateConfiguration", Drive, Dict[str, any]],
            ) -> "DriveInstance":
                return await self._update_func(instance.metadata.name or "", updates)

            return instance_update


class _SyncUpdateDescriptor:
    """Descriptor that provides both class-level and instance-level update functionality (sync)."""

    def __init__(self, update_func: Callable):
        self._update_func = update_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: SyncDriveInstance.update("name", updates)
            return self._update_func
        else:
            # Called on an instance: instance.update(updates)
            def instance_update(
                updates: Union["DriveCreateConfiguration", Drive, Dict[str, any]],
            ) -> "SyncDriveInstance":
                return self._update_func(instance.metadata.name or "", updates)

            return instance_update


class DriveCreateConfiguration:
    """Simplified configuration for creating drives with default values."""

    def __init__(
        self,
        name: str | None = None,
        display_name: str | None = None,
        labels: Dict[str, str] | None = None,
        size: int | None = None,  # Size in GB
        region: str | None = None,  # Region
    ):
        self.name = name
        self.display_name = display_name
        self.labels = labels
        self.size = size
        self.region = region

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "DriveCreateConfiguration":
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            labels=data.get("labels"),
            size=data.get("size"),
            region=data.get("region"),
        )


class DriveInstance:
    delete: "_AsyncDeleteDescriptor"

    def __init__(self, drive: Drive):
        self.drive = drive

    @property
    def metadata(self):
        return self.drive.metadata

    @property
    def spec(self):
        return self.drive.spec

    @property
    def status(self):
        return self.drive.status

    @property
    def name(self):
        return self.drive.metadata.name if self.drive.metadata else None

    @property
    def display_name(self):
        return self.drive.metadata.display_name if self.drive.metadata else None

    @property
    def size(self):
        return self.drive.spec.size if self.drive.spec else None

    @property
    def region(self):
        return self.drive.spec.region if self.drive.spec else None

    @classmethod
    async def create(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "DriveInstance":
        # Generate default values
        default_name = f"drive-{uuid.uuid4().hex[:8]}"
        default_size = 10  # 10GB

        # Handle different configuration types
        if isinstance(config, Drive):
            drive = config
        elif isinstance(config, DriveCreateConfiguration):
            drive = Drive(
                metadata=Metadata(
                    name=config.name or default_name,
                    display_name=config.display_name or config.name or default_name,
                    labels=config.labels,
                ),
                spec=DriveSpec(
                    size=config.size or default_size,
                    region=config.region or settings.region or UNSET,
                ),
            )
        elif isinstance(config, dict):
            drive_config = DriveCreateConfiguration.from_dict(config)
            drive = Drive(
                metadata=Metadata(
                    name=drive_config.name or default_name,
                    display_name=drive_config.display_name or drive_config.name or default_name,
                    labels=drive_config.labels,
                ),
                spec=DriveSpec(
                    size=drive_config.size or default_size,
                    region=drive_config.region or settings.region or UNSET,
                ),
            )
        else:
            raise ValueError(
                f"Invalid config type: {type(config)}. Expected DriveCreateConfiguration, Drive, or dict."
            )

        # Ensure required fields have defaults
        if not drive.metadata:
            drive.metadata = Metadata(name=default_name)
        if not drive.metadata.name:
            drive.metadata.name = default_name
        if not drive.spec:
            drive.spec = DriveSpec(size=default_size)
        if not drive.spec.size:
            drive.spec.size = default_size

        # Warn if region is not set
        if not drive.spec.region or drive.spec.region is UNSET:
            warnings.warn(
                "DriveInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the drive configuration or set the BL_REGION environment variable.",
                FutureWarning,
                stacklevel=2,
            )

        response = await create_drive(client=client, body=drive)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise DriveAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    async def get(cls, drive_name: str) -> "DriveInstance":
        response = await get_drive(drive_name=drive_name, client=client)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise DriveAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    async def list(cls) -> list["DriveInstance"]:
        response = await list_drives(client=client)
        return [cls(drive) for drive in response or []]

    @classmethod
    async def create_if_not_exists(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "DriveInstance":
        """Create a drive if it doesn't exist, otherwise return existing."""
        try:
            return await cls.create(config)
        except DriveAPIError as e:
            # Check if it's a 409 conflict error (drive already exists)
            if e.status_code == 409 or e.code in ["409", "DRIVE_ALREADY_EXISTS"]:
                # Extract name from different configuration types
                if isinstance(config, DriveCreateConfiguration):
                    name = config.name
                elif isinstance(config, dict):
                    name = config.get("name")
                elif isinstance(config, Drive):
                    name = config.metadata.name if config.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Drive name is required")

                drive_instance = await cls.get(name)
                return drive_instance
            raise


class SyncDriveInstance:
    delete: "_SyncDeleteDescriptor"

    """Synchronous drive instance for managing persistent storage."""

    def __init__(self, drive: Drive):
        self.drive = drive

    @property
    def metadata(self):
        return self.drive.metadata

    @property
    def spec(self):
        return self.drive.spec

    @property
    def status(self):
        return self.drive.status

    @property
    def name(self):
        return self.drive.metadata.name if self.drive.metadata else None

    @property
    def display_name(self):
        return self.drive.metadata.display_name if self.drive.metadata else None

    @property
    def size(self):
        return self.drive.spec.size if self.drive.spec else None

    @property
    def region(self):
        return self.drive.spec.region if self.drive.spec else None

    @classmethod
    def create(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "SyncDriveInstance":
        """Create a new drive synchronously."""
        # Generate default values
        default_name = f"drive-{uuid.uuid4().hex[:8]}"
        default_size = 10  # 10GB

        # Handle different configuration types
        if isinstance(config, Drive):
            drive = config
        elif isinstance(config, DriveCreateConfiguration):
            drive = Drive(
                metadata=Metadata(
                    name=config.name or default_name,
                    display_name=config.display_name or config.name or default_name,
                    labels=config.labels,
                ),
                spec=DriveSpec(
                    size=config.size or default_size,
                    region=config.region or settings.region or UNSET,
                ),
            )
        elif isinstance(config, dict):
            drive_config = DriveCreateConfiguration.from_dict(config)
            drive = Drive(
                metadata=Metadata(
                    name=drive_config.name or default_name,
                    display_name=drive_config.display_name or drive_config.name or default_name,
                    labels=drive_config.labels,
                ),
                spec=DriveSpec(
                    size=drive_config.size or default_size,
                    region=drive_config.region or settings.region or UNSET,
                ),
            )
        else:
            raise ValueError(
                f"Invalid config type: {type(config)}. Expected DriveCreateConfiguration, Drive, or dict."
            )

        # Ensure required fields have defaults
        if not drive.metadata:
            drive.metadata = Metadata(name=default_name)
        if not drive.metadata.name:
            drive.metadata.name = default_name
        if not drive.spec:
            drive.spec = DriveSpec(size=default_size)
        if not drive.spec.size:
            drive.spec.size = default_size

        # Warn if region is not set
        if not drive.spec.region or drive.spec.region is UNSET:
            warnings.warn(
                "SyncDriveInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the drive configuration or set the BL_REGION environment variable.",
                FutureWarning,
                stacklevel=2,
            )

        response = create_drive_sync(client=client, body=drive)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise DriveAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    def get(cls, drive_name: str) -> "SyncDriveInstance":
        """Get a drive by name synchronously."""
        response = get_drive_sync(drive_name=drive_name, client=client)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise DriveAPIError(message, status_code=status_code, code=response.error)
        return cls(response)

    @classmethod
    def list(cls) -> List["SyncDriveInstance"]:
        """List all drives synchronously."""
        response = list_drives_sync(client=client)
        return [cls(drive) for drive in response or []]

    @classmethod
    def create_if_not_exists(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "SyncDriveInstance":
        """Create a drive if it doesn't exist, otherwise return existing."""
        try:
            return cls.create(config)
        except DriveAPIError as e:
            # Check if it's a 409 conflict error (drive already exists)
            if e.status_code == 409 or e.code in ["409", "DRIVE_ALREADY_EXISTS"]:
                # Extract name from different configuration types
                if isinstance(config, DriveCreateConfiguration):
                    name = config.name
                elif isinstance(config, dict):
                    name = config.get("name")
                elif isinstance(config, Drive):
                    name = config.metadata.name if config.metadata else None
                else:
                    name = None

                if not name:
                    raise ValueError("Drive name is required")

                drive_instance = cls.get(name)
                return drive_instance
            raise


async def _delete_drive_by_name(drive_name: str) -> Drive:
    """Delete a drive by name (async)."""
    response = await delete_drive(drive_name=drive_name, client=client)
    return response


def _delete_drive_by_name_sync(drive_name: str) -> Drive:
    """Delete a drive by name (sync)."""
    response = delete_drive_sync(drive_name=drive_name, client=client)
    return response


async def _update_drive_by_name(
    drive_name: str, updates: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
) -> "DriveInstance":
    """Update a drive by name (async)."""
    # Get the current drive
    drive_instance = await DriveInstance.get(drive_name)
    current_drive = drive_instance.drive

    # Build the update body
    if isinstance(updates, Drive):
        new_metadata = updates.metadata
        new_spec = updates.spec
    elif isinstance(updates, DriveCreateConfiguration):
        new_metadata = Metadata(
            name=current_drive.metadata.name if current_drive.metadata else drive_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = DriveSpec(
            size=updates.size,
            region=updates.region,
        )
    elif isinstance(updates, dict):
        config = DriveCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_drive.metadata.name if current_drive.metadata else drive_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = DriveSpec(
            size=config.size,
            region=config.region,
        )
    else:
        raise ValueError(
            f"Invalid updates type: {type(updates)}. Expected DriveCreateConfiguration, Drive, or dict."
        )

    # Merge current values with updates
    merged_metadata = Metadata(
        name=current_drive.metadata.name if current_drive.metadata else drive_name,
        display_name=new_metadata.display_name
        if new_metadata and new_metadata.display_name
        else (current_drive.metadata.display_name if current_drive.metadata else None),
        labels=new_metadata.labels
        if new_metadata and new_metadata.labels
        else (current_drive.metadata.labels if current_drive.metadata else None),
    )

    merged_spec = DriveSpec(
        size=new_spec.size
        if new_spec and new_spec.size
        else (current_drive.spec.size if current_drive.spec else None),
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_drive.spec.region if current_drive.spec else None),
    )

    body = Drive(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = await update_drive(drive_name=drive_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise DriveAPIError(message, status_code=status_code, code=response.error)
    # This is for safe update
    await asyncio.sleep(0.5)
    return DriveInstance(response)


def _update_drive_by_name_sync(
    drive_name: str, updates: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
) -> "SyncDriveInstance":
    """Update a drive by name (sync)."""
    # Get the current drive
    drive_instance = SyncDriveInstance.get(drive_name)
    current_drive = drive_instance.drive

    # Build the update body
    if isinstance(updates, Drive):
        new_metadata = updates.metadata
        new_spec = updates.spec
    elif isinstance(updates, DriveCreateConfiguration):
        new_metadata = Metadata(
            name=current_drive.metadata.name if current_drive.metadata else drive_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = DriveSpec(
            size=updates.size,
            region=updates.region,
        )
    elif isinstance(updates, dict):
        config = DriveCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_drive.metadata.name if current_drive.metadata else drive_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = DriveSpec(
            size=config.size,
            region=config.region,
        )
    else:
        raise ValueError(
            f"Invalid updates type: {type(updates)}. Expected DriveCreateConfiguration, Drive, or dict."
        )

    # Merge current values with updates
    merged_metadata = Metadata(
        name=current_drive.metadata.name if current_drive.metadata else drive_name,
        display_name=new_metadata.display_name
        if new_metadata and new_metadata.display_name
        else (current_drive.metadata.display_name if current_drive.metadata else None),
        labels=new_metadata.labels
        if new_metadata and new_metadata.labels
        else (current_drive.metadata.labels if current_drive.metadata else None),
    )

    merged_spec = DriveSpec(
        size=new_spec.size
        if new_spec and new_spec.size
        else (current_drive.spec.size if current_drive.spec else None),
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_drive.spec.region if current_drive.spec else None),
    )

    body = Drive(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = update_drive_sync(drive_name=drive_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise DriveAPIError(message, status_code=status_code, code=response.error)
    # This is for safe update
    time.sleep(0.5)
    return SyncDriveInstance(response)


# Assign the delete descriptors to support both class-level and instance-level calls
DriveInstance.delete = _AsyncDeleteDescriptor(_delete_drive_by_name)
SyncDriveInstance.delete = _SyncDeleteDescriptor(_delete_drive_by_name_sync)

# Assign the update descriptors to support both class-level and instance-level calls
DriveInstance.update = _AsyncUpdateDescriptor(_update_drive_by_name)
SyncDriveInstance.update = _SyncUpdateDescriptor(_update_drive_by_name_sync)
