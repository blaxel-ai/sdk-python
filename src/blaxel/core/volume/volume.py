import asyncio
import time
import uuid
import warnings
from typing import Callable, Dict, Union

from ..client.api.volumes.create_volume import asyncio as create_volume
from ..client.api.volumes.create_volume import sync as create_volume_sync
from ..client.api.volumes.delete_volume import asyncio as delete_volume
from ..client.api.volumes.delete_volume import sync as delete_volume_sync
from ..client.api.volumes.get_volume import asyncio as get_volume
from ..client.api.volumes.get_volume import sync as get_volume_sync
from ..client.api.volumes.list_volumes import asyncio as list_volumes
from ..client.api.volumes.list_volumes import sync as list_volumes_sync
from ..client.api.volumes.update_volume import asyncio as update_volume
from ..client.api.volumes.update_volume import sync as update_volume_sync
from ..client.client import client
from ..client.models import Metadata, Volume, VolumeSpec
from ..client.models.error import Error
from ..client.pagination import (
    AsyncPaginatedList,
    PaginatedList,
    make_async_paginated_list,
    make_paginated_list,
    normalize_cursor,
)
from ..client.types import UNSET
from ..common.settings import settings
from ..errors import _APIError


class VolumeAPIError(_APIError):
    """Exception raised when volume API returns an error."""


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
                """Delete this volume; see ``VolumeInstance.delete("name")`` for details."""
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
                """Delete this volume; see ``SyncVolumeInstance.delete("name")`` for details."""
                return self._delete_func(instance.metadata.name or "")

            return instance_delete


class _AsyncUpdateDescriptor:
    """Descriptor that provides both class-level and instance-level update functionality."""

    def __init__(self, update_func: Callable):
        self._update_func = update_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: VolumeInstance.update("name", updates)
            return self._update_func
        else:
            # Called on an instance: instance.update(updates)
            async def instance_update(
                updates: Union["VolumeCreateConfiguration", Volume, Dict[str, any]],
            ) -> "VolumeInstance":
                """Update this volume; see ``VolumeInstance.update("name", updates)``."""
                return await self._update_func(instance.metadata.name or "", updates)

            return instance_update


class _SyncUpdateDescriptor:
    """Descriptor that provides both class-level and instance-level update functionality (sync)."""

    def __init__(self, update_func: Callable):
        self._update_func = update_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: SyncVolumeInstance.update("name", updates)
            return self._update_func
        else:
            # Called on an instance: instance.update(updates)
            def instance_update(
                updates: Union["VolumeCreateConfiguration", Volume, Dict[str, any]],
            ) -> "SyncVolumeInstance":
                """Update this volume; see ``SyncVolumeInstance.update("name", updates)``."""
                return self._update_func(instance.metadata.name or "", updates)

            return instance_update


class VolumeCreateConfiguration:
    """Simplified configuration for creating volumes with default values.

    Args:
        name: Volume name: lowercase letters, digits and hyphens, at most 49
            characters. Defaults to ``volume-<8 hex characters>``.
        display_name: Human-readable name. Defaults to the name.
        labels: Key-value labels.
        size: Size in MB. Defaults to 1024. It can grow later, never shrink.
        region: Region such as ``us-pdx-1``. Defaults to ``BL_REGION``. It
            cannot change after creation.
        template: Optional volume template to start from. It cannot change
            after creation.
    """

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
        """Build a configuration from a dict with the same keys as the constructor."""
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            labels=data.get("labels"),
            size=data.get("size"),
            region=data.get("region"),
            template=data.get("template"),
        )


class VolumeInstance:
    """A persistent volume: block storage that outlives the sandboxes using it.

    A volume is attached to one sandbox at a time, through the sandbox's
    ``volumes`` setting at creation (``{"name": ..., "mount_path": ...}``).
    Creating a sandbox with a volume already attached elsewhere fails with
    HTTP 409, and an attached volume cannot be deleted. Create it in the
    region of the sandboxes that will use it. ``delete`` and ``update`` work
    on the class with a name, ``await VolumeInstance.delete("name")``, and on
    an instance, ``await volume.delete()``.

    Example:
        ```python
        volume = await VolumeInstance.create_if_not_exists(
            {"name": "agent-data", "size": 2048, "region": "us-pdx-1"}
        )
        sandbox = await SandboxInstance.create(
            {
                "name": "agent",
                "region": "us-pdx-1",
                "volumes": [{"name": "agent-data", "mount_path": "/data"}],
            }
        )
        ```
    """

    delete: "_AsyncDeleteDescriptor"

    def __init__(self, volume: Volume):
        self.volume = volume

    @property
    def metadata(self):
        """Volume metadata: ``name``, ``display_name``, ``labels``."""
        return self.volume.metadata

    @property
    def spec(self):
        """Volume spec: ``size`` in MB, ``region`` and ``template``."""
        return self.volume.spec

    @property
    def status(self):
        """Volume status as reported by the API."""
        return self.volume.status

    @property
    def name(self):
        """Volume name, or None when the record has no metadata."""
        return self.volume.metadata.name if self.volume.metadata else None

    @property
    def display_name(self):
        """Human-readable name, or None."""
        return self.volume.metadata.display_name if self.volume.metadata else None

    @property
    def size(self):
        """Size in MB, or None."""
        return self.volume.spec.size if self.volume.spec else None

    @property
    def region(self):
        """Region, or None."""
        return self.volume.spec.region if self.volume.spec else None

    @property
    def template(self):
        """Template the volume was created from, or None."""
        return self.volume.spec.template if self.volume.spec else None

    @classmethod
    async def create(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "VolumeInstance":
        """Create a volume.

        Missing settings get defaults: name ``volume-<8 hex characters>``,
        size 1024 MB and the region from ``BL_REGION``. Without a region a
        ``FutureWarning`` is shown and the platform picks one. Creating a name
        that is already taken fails with HTTP 409; use
        :meth:`create_if_not_exists` to reuse it instead.

        Args:
            config: A ``VolumeCreateConfiguration``, a dict with ``name``,
                ``display_name``, ``labels``, ``size`` (MB), ``region`` and
                ``template``, or a full ``Volume`` model.

        Returns:
            The new ``VolumeInstance``.

        Raises:
            ValueError: When ``config`` has an unsupported type.
            VolumeAPIError: When the API rejects the creation, for example
                HTTP 409 for a name in use. ``status_code`` and ``code`` carry
                the details.

        Example:
            ```python
            volume = await VolumeInstance.create({"name": "agent-data", "region": "us-pdx-1"})
            ```
        """
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
                    region=config.region or settings.region or UNSET,
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
                    region=volume_config.region or settings.region or UNSET,
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

        # Warn if region is not set
        if not volume.spec.region or volume.spec.region is UNSET:
            warnings.warn(
                "VolumeInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the volume configuration or set the BL_REGION environment variable.",
                FutureWarning,
                stacklevel=2,
            )

        response = await create_volume(client=client, body=volume)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    async def get(cls, volume_name: str) -> "VolumeInstance":
        """Get a volume by name.

        Args:
            volume_name: The volume name.

        Returns:
            A ``VolumeInstance`` with the current record.

        Raises:
            VolumeAPIError: When the volume does not exist (``status_code``
                404) or the API rejects the request.
        """
        response = await get_volume(volume_name=volume_name, client=client)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    async def list(
        cls, limit: int = 50, cursor: str | None = None
    ) -> AsyncPaginatedList["VolumeInstance"]:
        """List one page of volumes.

        Args:
            limit: Maximum number of volumes to return in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.

        Returns:
            AsyncPaginatedList[VolumeInstance]: A list-like page with `.data`, `.meta`,
            `.has_more`, `.next_cursor`, `.next_page()`, and `.auto_paging_iter()`.

        Raises:
            VolumeAPIError: When the API rejects the request.

        Example:
            ```python
            page = await VolumeInstance.list(limit=50)

            for volume in page.data:
                print(volume.name)

            if page.has_more:
                next_page = await page.next_page()

            async for volume in page.auto_paging_iter():
                print(volume.name)
            ```
        """

        async def fetch_page(page_cursor: str | None):
            response = await list_volumes(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            if isinstance(response, Error):
                status_code = int(response.code) if response.code is not UNSET else None
                message = response.message if response.message is not UNSET else response.error
                raise VolumeAPIError(
                    message, status_code=status_code, code=response.error, error=response
                )
            return make_async_paginated_list(response, mapper=cls, fetch_next=fetch_page)

        return await fetch_page(cursor)

    @classmethod
    async def create_if_not_exists(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "VolumeInstance":
        """Create a volume if it doesn't exist, otherwise return existing.

        Tries :meth:`create` and, when the name is taken (HTTP 409), returns
        the existing volume as it is: the requested size, region and other
        settings are not applied to it. Use :meth:`update` to grow it.

        Args:
            config: The volume to create, in any form :meth:`create` accepts.
                It needs a name.

        Returns:
            The existing or new ``VolumeInstance``.

        Raises:
            ValueError: When the name is taken and ``config`` has no name.
            VolumeAPIError: When the API rejects the request.
        """
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
    """Synchronous volume instance for managing persistent storage.

    Same behavior as ``VolumeInstance``, without ``await``. A volume is
    attached to one sandbox at a time, through the sandbox's ``volumes``
    setting at creation. ``delete`` and ``update`` work on the class with a
    name, ``SyncVolumeInstance.delete("name")``, and on an instance,
    ``volume.delete()``.

    Example:
        ```python
        volume = SyncVolumeInstance.create_if_not_exists(
            {"name": "agent-data", "size": 2048, "region": "us-pdx-1"}
        )
        ```
    """

    delete: "_SyncDeleteDescriptor"

    def __init__(self, volume: Volume):
        self.volume = volume

    @property
    def metadata(self):
        """Volume metadata: ``name``, ``display_name``, ``labels``."""
        return self.volume.metadata

    @property
    def spec(self):
        """Volume spec: ``size`` in MB, ``region`` and ``template``."""
        return self.volume.spec

    @property
    def status(self):
        """Volume status as reported by the API."""
        return self.volume.status

    @property
    def name(self):
        """Volume name, or None when the record has no metadata."""
        return self.volume.metadata.name if self.volume.metadata else None

    @property
    def display_name(self):
        """Human-readable name, or None."""
        return self.volume.metadata.display_name if self.volume.metadata else None

    @property
    def size(self):
        """Size in MB, or None."""
        return self.volume.spec.size if self.volume.spec else None

    @property
    def region(self):
        """Region, or None."""
        return self.volume.spec.region if self.volume.spec else None

    @property
    def template(self):
        """Template the volume was created from, or None."""
        return self.volume.spec.template if self.volume.spec else None

    @classmethod
    def create(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "SyncVolumeInstance":
        """Create a new volume synchronously.

        Missing settings get defaults: name ``volume-<8 hex characters>``,
        size 1024 MB and the region from ``BL_REGION``. Without a region a
        ``FutureWarning`` is shown and the platform picks one. Creating a name
        that is already taken fails with HTTP 409; use
        :meth:`create_if_not_exists` to reuse it instead.

        Args:
            config: A ``VolumeCreateConfiguration``, a dict with ``name``,
                ``display_name``, ``labels``, ``size`` (MB), ``region`` and
                ``template``, or a full ``Volume`` model.

        Returns:
            The new ``SyncVolumeInstance``.

        Raises:
            ValueError: When ``config`` has an unsupported type.
            VolumeAPIError: When the API rejects the creation, for example
                HTTP 409 for a name in use. ``status_code`` and ``code`` carry
                the details.

        Example:
            ```python
            volume = SyncVolumeInstance.create({"name": "agent-data", "region": "us-pdx-1"})
            ```
        """
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
                    region=config.region or settings.region or UNSET,
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
                    region=volume_config.region or settings.region or UNSET,
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

        # Warn if region is not set
        if not volume.spec.region or volume.spec.region is UNSET:
            warnings.warn(
                "SyncVolumeInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the volume configuration or set the BL_REGION environment variable.",
                FutureWarning,
                stacklevel=2,
            )

        response = create_volume_sync(client=client, body=volume)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    def get(cls, volume_name: str) -> "SyncVolumeInstance":
        """Get a volume by name synchronously.

        Args:
            volume_name: The volume name.

        Returns:
            A ``SyncVolumeInstance`` with the current record.

        Raises:
            VolumeAPIError: When the volume does not exist (``status_code``
                404) or the API rejects the request.
        """
        response = get_volume_sync(volume_name=volume_name, client=client)
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise VolumeAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    def list(
        cls, limit: int = 50, cursor: str | None = None
    ) -> PaginatedList["SyncVolumeInstance"]:
        """List one page of volumes synchronously.

        Args:
            limit: Maximum number of volumes to return in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.

        Returns:
            PaginatedList[SyncVolumeInstance]: A list-like page with `.data`, `.meta`,
            `.has_more`, `.next_cursor`, `.next_page()`, and `.auto_paging_iter()`.

        Raises:
            VolumeAPIError: When the API rejects the request.

        Example:
            ```python
            page = SyncVolumeInstance.list(limit=50)

            for volume in page.data:
                print(volume.name)

            if page.has_more:
                next_page = page.next_page()

            for volume in page.auto_paging_iter():
                print(volume.name)
            ```
        """

        def fetch_page(page_cursor: str | None):
            response = list_volumes_sync(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            if isinstance(response, Error):
                status_code = int(response.code) if response.code is not UNSET else None
                message = response.message if response.message is not UNSET else response.error
                raise VolumeAPIError(
                    message, status_code=status_code, code=response.error, error=response
                )
            return make_paginated_list(response, mapper=cls, fetch_next=fetch_page)

        return fetch_page(cursor)

    @classmethod
    def create_if_not_exists(
        cls, config: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
    ) -> "SyncVolumeInstance":
        """Create a volume if it doesn't exist, otherwise return existing.

        Tries :meth:`create` and, when the name is taken (HTTP 409), returns
        the existing volume as it is: the requested size, region and other
        settings are not applied to it. Use :meth:`update` to grow it.

        Args:
            config: The volume to create, in any form :meth:`create` accepts.
                It needs a name.

        Returns:
            The existing or new ``SyncVolumeInstance``.

        Raises:
            ValueError: When the name is taken and ``config`` has no name.
            VolumeAPIError: When the API rejects the request.
        """
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
    """Delete a volume by name (async).

    Exposed as ``await VolumeInstance.delete("name")`` and as ``await volume.delete()`` on
    an instance. The data on the volume is lost. A volume attached to a
    sandbox cannot be deleted: the API answers HTTP 400, raised as
    ``blaxel.core.client.errors.UnexpectedStatus``; delete the sandbox first.

    Args:
        volume_name: The volume name.

    Returns:
        The deleted ``Volume`` record. Its status is ``DELETING`` until the
        deletion finishes; after that, ``get`` raises a 404.

    Raises:
        VolumeAPIError: When the volume does not exist (``status_code`` 404)
            or the API rejects the request.
        blaxel.core.client.errors.UnexpectedStatus: HTTP 400 when the volume
            is attached to a sandbox.
    """
    response = await delete_volume(volume_name=volume_name, client=client)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise VolumeAPIError(message, status_code=status_code, code=response.error, error=response)
    if response is None:
        raise VolumeAPIError(f"Failed to delete volume {volume_name}")
    return response


def _delete_volume_by_name_sync(volume_name: str) -> Volume:
    """Delete a volume by name (sync).

    Exposed as ``SyncVolumeInstance.delete("name")`` and as ``volume.delete()`` on
    an instance. The data on the volume is lost. A volume attached to a
    sandbox cannot be deleted: the API answers HTTP 400, raised as
    ``blaxel.core.client.errors.UnexpectedStatus``; delete the sandbox first.

    Args:
        volume_name: The volume name.

    Returns:
        The deleted ``Volume`` record. Its status is ``DELETING`` until the
        deletion finishes; after that, ``get`` raises a 404.

    Raises:
        VolumeAPIError: When the volume does not exist (``status_code`` 404)
            or the API rejects the request.
        blaxel.core.client.errors.UnexpectedStatus: HTTP 400 when the volume
            is attached to a sandbox.
    """
    response = delete_volume_sync(volume_name=volume_name, client=client)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise VolumeAPIError(message, status_code=status_code, code=response.error, error=response)
    if response is None:
        raise VolumeAPIError(f"Failed to delete volume {volume_name}")
    return response


async def _update_volume_by_name(
    volume_name: str, updates: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
) -> "VolumeInstance":
    """Update a volume by name (async).

    Exposed as ``await VolumeInstance.update("name", updates)`` and as
    ``await volume.update(updates)`` on an instance. The volume is read first;
    fields given in ``updates`` replace the current ones (``labels`` as a
    whole) and the others are kept. Only ``size``, ``display_name`` and
    ``labels`` can change: the size can grow but never shrink, and the region
    and template are fixed at creation. The API rejects other changes with
    HTTP 400, raised as ``blaxel.core.client.errors.UnexpectedStatus``. The
    call waits 0.5 seconds after the update before returning.

    Args:
        volume_name: The volume name.
        updates: A ``VolumeCreateConfiguration``, a dict with the same keys,
            or a ``Volume`` model.

    Returns:
        The updated ``VolumeInstance``.

    Raises:
        ValueError: When ``updates`` has an unsupported type.
        VolumeAPIError: When the volume does not exist.
        blaxel.core.client.errors.UnexpectedStatus: When the API rejects the
            update, such as a smaller size or a new region.

    Example:
        ```python
        volume = await VolumeInstance.update("agent-data", {"size": 4096})
        ```
    """
    # Get the current volume
    volume_instance = await VolumeInstance.get(volume_name)
    current_volume = volume_instance.volume

    # Build the update body
    if isinstance(updates, Volume):
        new_metadata = updates.metadata
        new_spec = updates.spec
    elif isinstance(updates, VolumeCreateConfiguration):
        new_metadata = Metadata(
            name=current_volume.metadata.name if current_volume.metadata else volume_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = VolumeSpec(
            size=updates.size,
            region=updates.region,
            template=updates.template,
        )
    elif isinstance(updates, dict):
        config = VolumeCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_volume.metadata.name if current_volume.metadata else volume_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = VolumeSpec(
            size=config.size,
            region=config.region,
            template=config.template,
        )
    else:
        raise ValueError(
            f"Invalid updates type: {type(updates)}. Expected VolumeCreateConfiguration, Volume, or dict."
        )

    # Merge current values with updates
    merged_metadata = Metadata(
        name=current_volume.metadata.name if current_volume.metadata else volume_name,
        display_name=new_metadata.display_name
        if new_metadata and new_metadata.display_name
        else (current_volume.metadata.display_name if current_volume.metadata else None),
        labels=new_metadata.labels
        if new_metadata and new_metadata.labels
        else (current_volume.metadata.labels if current_volume.metadata else None),
    )

    merged_spec = VolumeSpec(
        size=new_spec.size
        if new_spec and new_spec.size
        else (current_volume.spec.size if current_volume.spec else None),
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_volume.spec.region if current_volume.spec else None),
        template=new_spec.template
        if new_spec and new_spec.template
        else (current_volume.spec.template if current_volume.spec else None),
    )

    body = Volume(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = await update_volume(volume_name=volume_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise VolumeAPIError(message, status_code=status_code, code=response.error, error=response)
    # This is for safe update
    await asyncio.sleep(0.5)
    return VolumeInstance(response)


def _update_volume_by_name_sync(
    volume_name: str, updates: Union[VolumeCreateConfiguration, Volume, Dict[str, any]]
) -> "SyncVolumeInstance":
    """Update a volume by name (sync).

    Exposed as ``SyncVolumeInstance.update("name", updates)`` and as
    ``volume.update(updates)`` on an instance. The volume is read first;
    fields given in ``updates`` replace the current ones (``labels`` as a
    whole) and the others are kept. Only ``size``, ``display_name`` and
    ``labels`` can change: the size can grow but never shrink, and the region
    and template are fixed at creation. The API rejects other changes with
    HTTP 400, raised as ``blaxel.core.client.errors.UnexpectedStatus``. The
    call waits 0.5 seconds after the update before returning.

    Args:
        volume_name: The volume name.
        updates: A ``VolumeCreateConfiguration``, a dict with the same keys,
            or a ``Volume`` model.

    Returns:
        The updated ``SyncVolumeInstance``.

    Raises:
        ValueError: When ``updates`` has an unsupported type.
        VolumeAPIError: When the volume does not exist.
        blaxel.core.client.errors.UnexpectedStatus: When the API rejects the
            update, such as a smaller size or a new region.

    Example:
        ```python
        volume = SyncVolumeInstance.update("agent-data", {"size": 4096})
        ```
    """
    # Get the current volume
    volume_instance = SyncVolumeInstance.get(volume_name)
    current_volume = volume_instance.volume

    # Build the update body
    if isinstance(updates, Volume):
        new_metadata = updates.metadata
        new_spec = updates.spec
    elif isinstance(updates, VolumeCreateConfiguration):
        new_metadata = Metadata(
            name=current_volume.metadata.name if current_volume.metadata else volume_name,
            display_name=updates.display_name,
            labels=updates.labels,
        )
        new_spec = VolumeSpec(
            size=updates.size,
            region=updates.region,
            template=updates.template,
        )
    elif isinstance(updates, dict):
        config = VolumeCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_volume.metadata.name if current_volume.metadata else volume_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = VolumeSpec(
            size=config.size,
            region=config.region,
            template=config.template,
        )
    else:
        raise ValueError(
            f"Invalid updates type: {type(updates)}. Expected VolumeCreateConfiguration, Volume, or dict."
        )

    # Merge current values with updates
    merged_metadata = Metadata(
        name=current_volume.metadata.name if current_volume.metadata else volume_name,
        display_name=new_metadata.display_name
        if new_metadata and new_metadata.display_name
        else (current_volume.metadata.display_name if current_volume.metadata else None),
        labels=new_metadata.labels
        if new_metadata and new_metadata.labels
        else (current_volume.metadata.labels if current_volume.metadata else None),
    )

    merged_spec = VolumeSpec(
        size=new_spec.size
        if new_spec and new_spec.size
        else (current_volume.spec.size if current_volume.spec else None),
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_volume.spec.region if current_volume.spec else None),
        template=new_spec.template
        if new_spec and new_spec.template
        else (current_volume.spec.template if current_volume.spec else None),
    )

    body = Volume(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = update_volume_sync(volume_name=volume_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise VolumeAPIError(message, status_code=status_code, code=response.error, error=response)
    # This is for safe update
    time.sleep(0.5)
    return SyncVolumeInstance(response)


# Assign the delete descriptors to support both class-level and instance-level calls
VolumeInstance.delete = _AsyncDeleteDescriptor(_delete_volume_by_name)
SyncVolumeInstance.delete = _SyncDeleteDescriptor(_delete_volume_by_name_sync)

# Assign the update descriptors to support both class-level and instance-level calls
VolumeInstance.update = _AsyncUpdateDescriptor(_update_volume_by_name)
SyncVolumeInstance.update = _SyncUpdateDescriptor(_update_volume_by_name_sync)
