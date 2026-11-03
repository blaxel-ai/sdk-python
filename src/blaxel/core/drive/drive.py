import asyncio
import time
import uuid
import warnings
from typing import Callable, Dict, Union

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
from ..client.errors import UnexpectedStatus
from ..client.models import Drive, DriveSpec, Metadata
from ..client.models.error import Error
from ..client.pagination import (
    AsyncPaginatedList,
    PaginatedList,
    make_async_paginated_list,
    make_paginated_list,
    normalize_cursor,
)
from ..client.types import UNSET, Unset
from ..common.settings import settings
from ..errors import _APIError


class DriveAPIError(_APIError):
    """Exception raised when drive API returns an error."""


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
                """Delete this drive; see ``DriveInstance.delete("name")`` for details."""
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
                """Delete this drive; see ``SyncDriveInstance.delete("name")`` for details."""
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
                """Update this drive; see ``DriveInstance.update("name", updates)``."""
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
                """Update this drive; see ``SyncDriveInstance.update("name", updates)``."""
                return self._update_func(instance.metadata.name or "", updates)

            return instance_update


class DriveCreateConfiguration:
    """Simplified configuration for creating drives with default values.

    Args:
        name: Drive name: lowercase letters, digits and hyphens, at most 49
            characters. Defaults to ``drive-<8 hex characters>``.
        display_name: Human-readable name. Defaults to the name.
        labels: Key-value labels.
        size: Deprecated and ignored: drives have no size limit.
        region: Region such as ``us-pdx-1``. Defaults to ``BL_REGION``. It
            cannot change after creation.
        permissions: Optional access rules, at most 3. Each is a dict with
            ``labels`` (the workload must have all of them), ``path`` (a
            subfolder, default ``/``) and ``mode`` (``"read"`` or
            ``"read-write"``, the default). A workload gets access when any
            rule matches. Without rules, every workload in the workspace can
            access the drive.
    """

    def __init__(
        self,
        name: str | None = None,
        display_name: str | None = None,
        labels: Dict[str, str] | None = None,
        size: int | None = None,  # Deprecated: drives have no size limit, this is ignored
        region: str | None = None,  # Region
        permissions: list | None = None,
    ):
        self.name = name
        self.display_name = display_name
        self.labels = labels
        self.size = size
        self.region = region
        self.permissions = permissions

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "DriveCreateConfiguration":
        """Build a configuration from a dict with the same keys as the constructor."""
        return cls(
            name=data.get("name"),
            display_name=data.get("display_name"),
            labels=data.get("labels"),
            size=data.get("size"),
            region=data.get("region"),
            permissions=data.get("permissions"),
        )


class DriveInstance:
    """A drive: shared file storage that sandboxes mount while they run.

    Unlike a volume, a drive is mounted into a running sandbox with
    ``sandbox.drives.mount(...)`` (or at creation with ``mount_drives`` on
    ``SandboxInstance.create``), and several sandboxes can mount the same
    drive at once, read-write. Create it in the region of the sandboxes that
    will mount it; the region cannot change later. ``permissions`` (at most
    3) limit which workloads can reach the drive, by labels, path and mode.
    Drives must be enabled for the workspace, otherwise every call fails with
    HTTP 403. ``delete`` and ``update`` work on the class with a name,
    ``await DriveInstance.delete("name")``, and on an instance,
    ``await drive.delete()``.

    Example:
        ```python
        drive = await DriveInstance.create_if_not_exists(
            {"name": "shared-data", "region": "us-pdx-1"}
        )
        sandbox = await SandboxInstance.create({"name": "agent", "region": "us-pdx-1"})
        await sandbox.drives.mount("shared-data", "/mnt/shared")
        ```
    """

    delete: "_AsyncDeleteDescriptor"

    def __init__(self, drive: Drive):
        self.drive = drive

    @property
    def metadata(self):
        """Drive metadata: ``name``, ``display_name``, ``labels``."""
        return self.drive.metadata

    @property
    def spec(self):
        """Drive spec: ``region`` and ``permissions``."""
        return self.drive.spec

    @property
    def status(self):
        """Drive status as reported by the API."""
        return self.drive.status

    @property
    def name(self):
        """Drive name, or None when the record has no metadata."""
        return self.drive.metadata.name if self.drive.metadata else None

    @property
    def display_name(self):
        """Human-readable name, or None."""
        return self.drive.metadata.display_name if self.drive.metadata else None

    @property
    def size(self):
        """Deprecated: only legacy drives created with a size still report one."""
        if not self.drive.spec:
            return None
        return self.drive.spec.additional_properties.get("size")

    @property
    def region(self):
        """Region, or None."""
        return self.drive.spec.region if self.drive.spec else None

    @property
    def permissions(self):
        """Access rules, or None."""
        return self.drive.spec.permissions if self.drive.spec else None

    @classmethod
    async def create(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "DriveInstance":
        """Create a drive.

        Missing settings get defaults: name ``drive-<8 hex characters>`` and
        the region from ``BL_REGION``. Without a region a ``FutureWarning`` is
        shown and the platform picks one. Creating a name that is already
        taken, or whose drive is still being deleted, fails with HTTP 409;
        use :meth:`create_if_not_exists` to reuse it instead.

        Args:
            config: A ``DriveCreateConfiguration``, a dict with ``name``,
                ``display_name``, ``labels``, ``region`` and ``permissions``,
                or a full ``Drive`` model.

        Returns:
            The new ``DriveInstance``.

        Raises:
            ValueError: When ``config`` has an unsupported type.
            blaxel.core.client.errors.UnexpectedStatus: When the API rejects
                the drive: ``ConflictError`` (HTTP 409) for a name in use,
                HTTP 400 for invalid permissions or region, HTTP 403 when
                drives are not enabled for the workspace. The exception
                message shows only the status; the response body in
                ``e.content`` names the cause, such as "Drives feature is not
                enabled for this workspace".

        Example:
            ```python
            drive = await DriveInstance.create({"name": "shared-data", "region": "us-pdx-1"})
            ```
        """
        # Generate default values
        default_name = f"drive-{uuid.uuid4().hex[:8]}"

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
                    region=config.region or settings.region or UNSET,
                    permissions=config.permissions if config.permissions is not None else UNSET,
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
                    region=drive_config.region or settings.region or UNSET,
                    permissions=drive_config.permissions
                    if drive_config.permissions is not None
                    else UNSET,
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
            drive.spec = DriveSpec()

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
            raise DriveAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    async def get(cls, drive_name: str) -> "DriveInstance":
        """Get a drive by name.

        Args:
            drive_name: The drive name.

        Returns:
            A ``DriveInstance`` with the current record.

        Raises:
            DriveAPIError: With ``status_code`` 404 when the drive does not
                exist. An invalid API key (HTTP 401) is reported the same way.
            blaxel.core.client.errors.UnexpectedStatus: For other error
                statuses, such as HTTP 403 when drives are not enabled.
        """
        response = await get_drive(drive_name=drive_name, client=client)
        if response is None:
            raise DriveAPIError(
                f"Drive '{drive_name}' not found", status_code=404, code="NOT_FOUND"
            )
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise DriveAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    async def list(
        cls, limit: int = 50, cursor: str | None = None
    ) -> AsyncPaginatedList["DriveInstance"]:
        """List one page of drives.

        Args:
            limit: Maximum number of drives to return in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.

        Returns:
            AsyncPaginatedList[DriveInstance]: A list-like page with `.data`, `.meta`,
            `.has_more`, `.next_cursor`, `.next_page()`, and `.auto_paging_iter()`.

        Raises:
            blaxel.core.client.errors.UnexpectedStatus: When the API rejects
                the request, such as HTTP 403 when drives are not enabled.

        Example:
            ```python
            page = await DriveInstance.list(limit=50)

            for drive in page.data:
                print(drive.name)

            if page.has_more:
                next_page = await page.next_page()

            async for drive in page.auto_paging_iter():
                print(drive.name)
            ```
        """

        async def fetch_page(page_cursor: str | None):
            response = await list_drives(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            if isinstance(response, Error):
                status_code = int(response.code) if response.code is not UNSET else None
                message = response.message if response.message is not UNSET else response.error
                raise DriveAPIError(
                    message, status_code=status_code, code=response.error, error=response
                )
            return make_async_paginated_list(response, mapper=cls, fetch_next=fetch_page)

        return await fetch_page(cursor)

    @classmethod
    async def create_if_not_exists(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "DriveInstance":
        """Create a drive if it doesn't exist, otherwise return existing.

        Tries :meth:`create` and, when the name is taken (HTTP 409), returns
        the existing drive as it is: the requested labels, permissions and
        other settings are not applied to it. Use :meth:`update` to change
        them.

        Args:
            config: The drive to create, in any form :meth:`create` accepts.
                It needs a name.

        Returns:
            The existing or new ``DriveInstance``.

        Raises:
            ValueError: When the name is taken and ``config`` has no name.
            blaxel.core.client.errors.UnexpectedStatus: When the API rejects
                the request for another reason.
        """
        try:
            return await cls.create(config)
        except (DriveAPIError, UnexpectedStatus) as e:
            is_conflict = False
            if isinstance(e, DriveAPIError):
                is_conflict = e.status_code == 409 or e.code in ["409", "DRIVE_ALREADY_EXISTS"]
            elif isinstance(e, UnexpectedStatus):
                is_conflict = e.status_code == 409

            if is_conflict:
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

                return await cls.get(name)
            raise


class SyncDriveInstance:
    """Synchronous drive instance for managing persistent storage.

    Same behavior as ``DriveInstance``, without ``await``. Sandboxes mount a
    drive while they run, with ``sandbox.drives.mount(...)`` or ``mount_drives``
    on ``SyncSandboxInstance.create``, and several can mount it at once. ``delete`` and ``update`` work on the class with a
    name, ``SyncDriveInstance.delete("name")``, and on an instance,
    ``drive.delete()``.

    Example:
        ```python
        drive = SyncDriveInstance.create_if_not_exists(
            {"name": "shared-data", "region": "us-pdx-1"}
        )
        ```
    """

    delete: "_SyncDeleteDescriptor"

    def __init__(self, drive: Drive):
        self.drive = drive

    @property
    def metadata(self):
        """Drive metadata: ``name``, ``display_name``, ``labels``."""
        return self.drive.metadata

    @property
    def spec(self):
        """Drive spec: ``region`` and ``permissions``."""
        return self.drive.spec

    @property
    def status(self):
        """Drive status as reported by the API."""
        return self.drive.status

    @property
    def name(self):
        """Drive name, or None when the record has no metadata."""
        return self.drive.metadata.name if self.drive.metadata else None

    @property
    def display_name(self):
        """Human-readable name, or None."""
        return self.drive.metadata.display_name if self.drive.metadata else None

    @property
    def size(self):
        """Deprecated: only legacy drives created with a size still report one."""
        if not self.drive.spec:
            return None
        return self.drive.spec.additional_properties.get("size")

    @property
    def region(self):
        """Region, or None."""
        return self.drive.spec.region if self.drive.spec else None

    @property
    def permissions(self):
        """Access rules, or None."""
        return self.drive.spec.permissions if self.drive.spec else None

    @classmethod
    def create(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "SyncDriveInstance":
        """Create a new drive synchronously.

        Missing settings get defaults: name ``drive-<8 hex characters>`` and
        the region from ``BL_REGION``. Without a region a ``FutureWarning`` is
        shown and the platform picks one. Creating a name that is already
        taken, or whose drive is still being deleted, fails with HTTP 409;
        use :meth:`create_if_not_exists` to reuse it instead.

        Args:
            config: A ``DriveCreateConfiguration``, a dict with ``name``,
                ``display_name``, ``labels``, ``region`` and ``permissions``,
                or a full ``Drive`` model.

        Returns:
            The new ``SyncDriveInstance``.

        Raises:
            ValueError: When ``config`` has an unsupported type.
            blaxel.core.client.errors.UnexpectedStatus: When the API rejects
                the drive: ``ConflictError`` (HTTP 409) for a name in use,
                HTTP 400 for invalid permissions or region, HTTP 403 when
                drives are not enabled for the workspace. The exception
                message shows only the status; the response body in
                ``e.content`` names the cause, such as "Drives feature is not
                enabled for this workspace".

        Example:
            ```python
            drive = SyncDriveInstance.create({"name": "shared-data", "region": "us-pdx-1"})
            ```
        """
        # Generate default values
        default_name = f"drive-{uuid.uuid4().hex[:8]}"

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
                    region=config.region or settings.region or UNSET,
                    permissions=config.permissions if config.permissions is not None else UNSET,
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
                    region=drive_config.region or settings.region or UNSET,
                    permissions=drive_config.permissions
                    if drive_config.permissions is not None
                    else UNSET,
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
            drive.spec = DriveSpec()

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
            raise DriveAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    def get(cls, drive_name: str) -> "SyncDriveInstance":
        """Get a drive by name synchronously.

        Args:
            drive_name: The drive name.

        Returns:
            A ``SyncDriveInstance`` with the current record.

        Raises:
            DriveAPIError: With ``status_code`` 404 when the drive does not
                exist. An invalid API key (HTTP 401) is reported the same way.
            blaxel.core.client.errors.UnexpectedStatus: For other error
                statuses, such as HTTP 403 when drives are not enabled.
        """
        response = get_drive_sync(drive_name=drive_name, client=client)
        if response is None:
            raise DriveAPIError(
                f"Drive '{drive_name}' not found", status_code=404, code="NOT_FOUND"
            )
        if isinstance(response, Error):
            status_code = int(response.code) if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise DriveAPIError(
                message, status_code=status_code, code=response.error, error=response
            )
        return cls(response)

    @classmethod
    def list(cls, limit: int = 50, cursor: str | None = None) -> PaginatedList["SyncDriveInstance"]:
        """List one page of drives synchronously.

        Args:
            limit: Maximum number of drives to return in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.

        Returns:
            PaginatedList[SyncDriveInstance]: A list-like page with `.data`, `.meta`,
            `.has_more`, `.next_cursor`, `.next_page()`, and `.auto_paging_iter()`.

        Raises:
            blaxel.core.client.errors.UnexpectedStatus: When the API rejects
                the request, such as HTTP 403 when drives are not enabled.

        Example:
            ```python
            page = SyncDriveInstance.list(limit=50)

            for drive in page.data:
                print(drive.name)

            if page.has_more:
                next_page = page.next_page()

            for drive in page.auto_paging_iter():
                print(drive.name)
            ```
        """

        def fetch_page(page_cursor: str | None):
            response = list_drives_sync(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            if isinstance(response, Error):
                status_code = int(response.code) if response.code is not UNSET else None
                message = response.message if response.message is not UNSET else response.error
                raise DriveAPIError(
                    message, status_code=status_code, code=response.error, error=response
                )
            return make_paginated_list(response, mapper=cls, fetch_next=fetch_page)

        return fetch_page(cursor)

    @classmethod
    def create_if_not_exists(
        cls, config: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
    ) -> "SyncDriveInstance":
        """Create a drive if it doesn't exist, otherwise return existing.

        Tries :meth:`create` and, when the name is taken (HTTP 409), returns
        the existing drive as it is: the requested labels, permissions and
        other settings are not applied to it. Use :meth:`update` to change
        them.

        Args:
            config: The drive to create, in any form :meth:`create` accepts.
                It needs a name.

        Returns:
            The existing or new ``SyncDriveInstance``.

        Raises:
            ValueError: When the name is taken and ``config`` has no name.
            blaxel.core.client.errors.UnexpectedStatus: When the API rejects
                the request for another reason.
        """
        try:
            return cls.create(config)
        except (DriveAPIError, UnexpectedStatus) as e:
            is_conflict = False
            if isinstance(e, DriveAPIError):
                is_conflict = e.status_code == 409 or e.code in ["409", "DRIVE_ALREADY_EXISTS"]
            elif isinstance(e, UnexpectedStatus):
                is_conflict = e.status_code == 409

            if is_conflict:
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

                return cls.get(name)
            raise


async def _delete_drive_by_name(drive_name: str) -> Drive:
    """Delete a drive by name (async).

    Exposed as ``await DriveInstance.delete("name")`` and as ``await drive.delete()`` on
    an instance. Deletion runs in the background: the drive is marked
    ``DELETING`` and its files are removed. Reusing the name fails with
    HTTP 409 until the deletion finishes.

    Args:
        drive_name: The drive name.

    Returns:
        The API answer, a ``DeleteDriveResponse200`` with ``message``,
        ``name`` and ``status`` (``"DELETING"``), despite the ``Drive``
        annotation. None, without an error, when the drive does not exist
        (HTTP 404) or the API key is invalid (HTTP 401).

    Raises:
        blaxel.core.client.errors.UnexpectedStatus: For other error statuses,
            such as HTTP 403 when drives are not enabled.
    """
    response = await delete_drive(drive_name=drive_name, client=client)
    return response


def _delete_drive_by_name_sync(drive_name: str) -> Drive:
    """Delete a drive by name (sync).

    Exposed as ``SyncDriveInstance.delete("name")`` and as ``drive.delete()`` on
    an instance. Deletion runs in the background: the drive is marked
    ``DELETING`` and its files are removed. Reusing the name fails with
    HTTP 409 until the deletion finishes.

    Args:
        drive_name: The drive name.

    Returns:
        The API answer, a ``DeleteDriveResponse200`` with ``message``,
        ``name`` and ``status`` (``"DELETING"``), despite the ``Drive``
        annotation. None, without an error, when the drive does not exist
        (HTTP 404) or the API key is invalid (HTTP 401).

    Raises:
        blaxel.core.client.errors.UnexpectedStatus: For other error statuses,
            such as HTTP 403 when drives are not enabled.
    """
    response = delete_drive_sync(drive_name=drive_name, client=client)
    return response


async def _update_drive_by_name(
    drive_name: str, updates: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
) -> "DriveInstance":
    """Update a drive by name (async).

    Exposed as ``await DriveInstance.update("name", updates)`` and as
    ``await drive.update(updates)`` on an instance. The drive is read first;
    fields given in ``updates`` replace the current ones and the others are
    kept. ``labels`` and ``permissions`` are replaced as a whole. An empty
    ``labels`` dict keeps the current labels, while ``permissions=[]``
    removes every access rule. Only ``display_name``, ``labels`` and
    ``permissions`` can change: the region is fixed at creation, and the
    API rejects a new one with HTTP 400, raised as
    ``blaxel.core.client.errors.UnexpectedStatus``. The call waits 0.5
    seconds after the update before returning.

    Args:
        drive_name: The drive name.
        updates: A ``DriveCreateConfiguration``, a dict with the same keys,
            or a ``Drive`` model.

    Returns:
        The updated ``DriveInstance``.

    Raises:
        ValueError: When ``updates`` has an unsupported type.
        DriveAPIError: When the drive does not exist.
        blaxel.core.client.errors.UnexpectedStatus: When the API rejects the
            update, such as a new region or more than 3 permissions.

    Example:
        ```python
        drive = await DriveInstance.update(
            "shared-data",
            {"permissions": [{"labels": {"team": "data"}, "mode": "read"}]},
        )
        ```
    """
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
            region=updates.region,
            permissions=updates.permissions,
        )
    elif isinstance(updates, dict):
        config = DriveCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_drive.metadata.name if current_drive.metadata else drive_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = DriveSpec(
            region=config.region,
            permissions=config.permissions,
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
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_drive.spec.region if current_drive.spec else None),
        permissions=new_spec.permissions
        if new_spec
        and new_spec.permissions is not None
        and not isinstance(new_spec.permissions, Unset)
        else (current_drive.spec.permissions if current_drive.spec else UNSET),
    )

    body = Drive(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = await update_drive(drive_name=drive_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise DriveAPIError(message, status_code=status_code, code=response.error, error=response)
    # This is for safe update
    await asyncio.sleep(0.5)
    return DriveInstance(response)


def _update_drive_by_name_sync(
    drive_name: str, updates: Union[DriveCreateConfiguration, Drive, Dict[str, any]]
) -> "SyncDriveInstance":
    """Update a drive by name (sync).

    Exposed as ``SyncDriveInstance.update("name", updates)`` and as
    ``drive.update(updates)`` on an instance. The drive is read first;
    fields given in ``updates`` replace the current ones and the others are
    kept. ``labels`` and ``permissions`` are replaced as a whole. An empty
    ``labels`` dict keeps the current labels, while ``permissions=[]``
    removes every access rule. Only ``display_name``, ``labels`` and
    ``permissions`` can change: the region is fixed at creation, and the
    API rejects a new one with HTTP 400, raised as
    ``blaxel.core.client.errors.UnexpectedStatus``. The call waits 0.5
    seconds after the update before returning.

    Args:
        drive_name: The drive name.
        updates: A ``DriveCreateConfiguration``, a dict with the same keys,
            or a ``Drive`` model.

    Returns:
        The updated ``SyncDriveInstance``.

    Raises:
        ValueError: When ``updates`` has an unsupported type.
        DriveAPIError: When the drive does not exist.
        blaxel.core.client.errors.UnexpectedStatus: When the API rejects the
            update, such as a new region or more than 3 permissions.

    Example:
        ```python
        drive = SyncDriveInstance.update(
            "shared-data",
            {"permissions": [{"labels": {"team": "data"}, "mode": "read"}]},
        )
        ```
    """
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
            region=updates.region,
            permissions=updates.permissions,
        )
    elif isinstance(updates, dict):
        config = DriveCreateConfiguration.from_dict(updates)
        new_metadata = Metadata(
            name=current_drive.metadata.name if current_drive.metadata else drive_name,
            display_name=config.display_name,
            labels=config.labels,
        )
        new_spec = DriveSpec(
            region=config.region,
            permissions=config.permissions,
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
        region=new_spec.region
        if new_spec and new_spec.region
        else (current_drive.spec.region if current_drive.spec else None),
        permissions=new_spec.permissions
        if new_spec
        and new_spec.permissions is not None
        and not isinstance(new_spec.permissions, Unset)
        else (current_drive.spec.permissions if current_drive.spec else UNSET),
    )

    body = Drive(
        metadata=merged_metadata,
        spec=merged_spec,
    )

    response = update_drive_sync(drive_name=drive_name, client=client, body=body)
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise DriveAPIError(message, status_code=status_code, code=response.error, error=response)
    # This is for safe update
    time.sleep(0.5)
    return SyncDriveInstance(response)


# Assign the delete descriptors to support both class-level and instance-level calls
DriveInstance.delete = _AsyncDeleteDescriptor(_delete_drive_by_name)
SyncDriveInstance.delete = _SyncDeleteDescriptor(_delete_drive_by_name_sync)

# Assign the update descriptors to support both class-level and instance-level calls
DriveInstance.update = _AsyncUpdateDescriptor(_update_drive_by_name)
SyncDriveInstance.update = _SyncUpdateDescriptor(_update_drive_by_name_sync)
