from typing import Any, Callable, Dict, Union

from ..client.api.compute.create_snapshot import asyncio as create_snapshot
from ..client.api.compute.create_snapshot import sync as create_snapshot_sync
from ..client.api.compute.delete_snapshot import asyncio as delete_snapshot
from ..client.api.compute.delete_snapshot import sync as delete_snapshot_sync
from ..client.api.compute.fork_snapshot import asyncio as fork_snapshot
from ..client.api.compute.fork_snapshot import sync as fork_snapshot_sync
from ..client.api.compute.get_snapshot import asyncio as get_snapshot
from ..client.api.compute.get_snapshot import sync as get_snapshot_sync
from ..client.api.compute.list_snapshots import asyncio as list_snapshots
from ..client.api.compute.list_snapshots import sync as list_snapshots_sync
from ..client.client import client
from ..client.models import (
    SandboxForkRequest,
    SandboxForkResponse,
    SandboxSnapshot,
    SandboxSnapshotRequest,
    SandboxSnapshotSource,
    SandboxSnapshotSourceKind,
)
from ..client.models.error import Error
from ..client.pagination import (
    AsyncPaginatedList,
    PaginatedList,
    make_async_paginated_list,
    make_paginated_list,
    normalize_cursor,
)
from ..client.types import UNSET


class SnapshotAPIError(Exception):
    """Exception raised when the snapshot API returns an error."""

    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


def _unwrap(response, action: str, *, allow_none: bool = False):
    if isinstance(response, Error):
        status_code = int(response.code) if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise SnapshotAPIError(message, status_code=status_code, code=response.error)
    if response is None and not allow_none:
        raise SnapshotAPIError(f"Failed to {action}")
    return response


def _snapshot_request(
    config: Union[Dict[str, Any], SandboxSnapshotRequest],
) -> SandboxSnapshotRequest:
    """Build a create body from a configuration mapping.

    ``source.name`` is required; ``source.kind`` is optional and read as
    ``sandbox``, the only kind that can be captured today. ``name`` is optional
    and generated when omitted.
    """
    if isinstance(config, SandboxSnapshotRequest):
        return config
    source = config.get("source")
    if isinstance(source, SandboxSnapshotSource):
        request_source = source
    else:
        source_name = source.get("name") if isinstance(source, dict) else None
        if not source_name:
            raise ValueError("Snapshot source requires a name")
        kind = source.get("kind")
        # The generated model defaults ``kind`` to sandbox; left out of the
        # request, the control plane applies that same default itself.
        request_source = SandboxSnapshotSource(
            name=source_name,
            kind=SandboxSnapshotSourceKind(kind) if kind is not None else UNSET,
        )
    name = config.get("name")
    return (
        SandboxSnapshotRequest(source=request_source, name=name)
        if name is not None
        else SandboxSnapshotRequest(source=request_source)
    )


def _fork_body(
    target_name: str,
    target_type: str = "sandbox",
    port: int | None = None,
    traffic: int | None = None,
    custom_domain: str | None = None,
    prefix: str | None = None,
) -> SandboxForkRequest:
    body = SandboxForkRequest(target_name=target_name, target_type=target_type)
    if port is not None:
        body.port = port
    if traffic is not None:
        body.traffic = traffic
    if custom_domain is not None:
        body.custom_domain = custom_domain
    if prefix is not None:
        body.prefix = prefix
    return body


class _AsyncDeleteDescriptor:
    """Descriptor exposing delete as ``Snapshot.delete(name)`` and ``snapshot.delete()``."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func
        self.__doc__ = delete_func.__doc__

    def __get__(self, instance, owner):
        if instance is None:
            return self._delete_func

        async def instance_delete() -> None:
            return await self._delete_func(instance.name)

        instance_delete.__doc__ = self.__doc__
        return instance_delete


class _SyncDeleteDescriptor:
    """Descriptor exposing delete as ``SyncSnapshot.delete(name)`` and ``snapshot.delete()``."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func
        self.__doc__ = delete_func.__doc__

    def __get__(self, instance, owner):
        if instance is None:
            return self._delete_func

        def instance_delete() -> None:
            return self._delete_func(instance.name)

        instance_delete.__doc__ = self.__doc__
        return instance_delete


async def _delete_snapshot(snapshot_name: str) -> None:
    """Delete a snapshot.

    There is one snapshot object, so this removes it for the whole workspace,
    whether or not the sandbox it was captured from still exists.
    """
    response = await delete_snapshot(snapshot_name, client=client)
    _unwrap(response, f"delete snapshot {snapshot_name}", allow_none=True)


def _delete_snapshot_sync(snapshot_name: str) -> None:
    """Delete a snapshot.

    There is one snapshot object, so this removes it for the whole workspace,
    whether or not the sandbox it was captured from still exists.
    """
    response = delete_snapshot_sync(snapshot_name, client=client)
    _unwrap(response, f"delete snapshot {snapshot_name}", allow_none=True)


class _SnapshotBase:
    def __init__(self, snapshot: SandboxSnapshot):
        self.snapshot = snapshot

    @property
    def name(self) -> str:
        """Name of the snapshot, unique in the workspace."""
        return self.snapshot.name

    @property
    def id(self) -> str:
        """Identifier of the snapshot on the compute plane."""
        return self.snapshot.id

    @property
    def status(self):
        return self.snapshot.status

    @property
    def workspace(self):
        return self.snapshot.workspace

    @property
    def created_at(self):
        return self.snapshot.created_at

    @property
    def source(self):
        """The object the snapshot was captured from, and whether it still exists."""
        return self.snapshot.source

    @property
    def spec(self):
        """The configuration a fork of this snapshot runs with."""
        return self.snapshot.spec


class Snapshot(_SnapshotBase):
    """A snapshot is a workspace resource.

    It is captured from a sandbox, but it outlives it: deleting the sandbox it
    came from leaves the snapshot in place with ``source.deleted`` set, and it
    still carries what a fork needs to run.
    """

    delete = _AsyncDeleteDescriptor(_delete_snapshot)

    @classmethod
    async def create(cls, config: Union[Dict[str, Any], SandboxSnapshotRequest]) -> "Snapshot":
        """Capture a snapshot of a source object.

        Args:
            config: ``source`` of the snapshot and, optionally, its ``name``.

        Example:
            ```python
            snapshot = await Snapshot.create({
                "name": "my-snapshot",
                "source": {"name": "my-sandbox"},
            })
            ```
        """
        response = await create_snapshot(client=client, body=_snapshot_request(config))
        return cls(_unwrap(response, "create snapshot"))

    @classmethod
    async def get(cls, snapshot_name: str) -> "Snapshot":
        response = await get_snapshot(snapshot_name, client=client)
        return cls(_unwrap(response, f"get snapshot {snapshot_name}"))

    @classmethod
    async def list(
        cls, limit: int = 50, cursor: str | None = None
    ) -> AsyncPaginatedList["Snapshot"]:
        """List one page of the workspace's snapshots.

        Args:
            limit: Maximum number of snapshots to return in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.

        Returns:
            AsyncPaginatedList[Snapshot]: A list-like page with `.data`, `.meta`,
            `.has_more`, `.next_cursor`, `.next_page()`, and `.auto_paging_iter()`.
        """

        async def fetch_page(page_cursor: str | None):
            response = await list_snapshots(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            return make_async_paginated_list(
                _unwrap(response, "list snapshots"), mapper=cls, fetch_next=fetch_page
            )

        return await fetch_page(cursor)

    async def fork(
        self,
        target_name: str,
        target_type: str = "sandbox",
        port: int | None = None,
        traffic: int | None = None,
        custom_domain: str | None = None,
        prefix: str | None = None,
    ) -> SandboxForkResponse:
        """Create a sandbox or an application from this snapshot.

        This works after the sandbox the snapshot was captured from has been
        deleted.

        Args:
            target_name: Name of the sandbox/application to create.
            target_type: ``"sandbox"`` or ``"application"``.
            port: Port to expose from the created resource.
            traffic: Canary traffic percentage when forking into an application.
            custom_domain: Custom domain for the application fork.
            prefix: URL prefix for the application fork.
        """
        response = await fork_snapshot(
            self.name,
            client=client,
            body=_fork_body(target_name, target_type, port, traffic, custom_domain, prefix),
        )
        return _unwrap(response, f"fork snapshot {self.name}")


class SyncSnapshot(_SnapshotBase):
    """Synchronous counterpart of :class:`Snapshot`."""

    delete = _SyncDeleteDescriptor(_delete_snapshot_sync)

    @classmethod
    def create(cls, config: Union[Dict[str, Any], SandboxSnapshotRequest]) -> "SyncSnapshot":
        response = create_snapshot_sync(client=client, body=_snapshot_request(config))
        return cls(_unwrap(response, "create snapshot"))

    @classmethod
    def get(cls, snapshot_name: str) -> "SyncSnapshot":
        response = get_snapshot_sync(snapshot_name, client=client)
        return cls(_unwrap(response, f"get snapshot {snapshot_name}"))

    @classmethod
    def list(cls, limit: int = 50, cursor: str | None = None) -> PaginatedList["SyncSnapshot"]:
        def fetch_page(page_cursor: str | None):
            response = list_snapshots_sync(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            return make_paginated_list(
                _unwrap(response, "list snapshots"), mapper=cls, fetch_next=fetch_page
            )

        return fetch_page(cursor)

    def fork(
        self,
        target_name: str,
        target_type: str = "sandbox",
        port: int | None = None,
        traffic: int | None = None,
        custom_domain: str | None = None,
        prefix: str | None = None,
    ) -> SandboxForkResponse:
        response = fork_snapshot_sync(
            self.name,
            client=client,
            body=_fork_body(target_name, target_type, port, traffic, custom_domain, prefix),
        )
        return _unwrap(response, f"fork snapshot {self.name}")
