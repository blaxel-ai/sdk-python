from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_snapshot_source import SandboxSnapshotSource
    from ..models.sandbox_snapshot_spec import SandboxSnapshotSpec


T = TypeVar("T", bound="SandboxSnapshot")


@_attrs_define
class SandboxSnapshot:
    """A point-in-time snapshot of a sandbox. It is a workspace-level object: it outlives the sandbox it was captured from,
    and can be restored onto a sandbox or forked into a new sandbox or application on its own.

        Attributes:
            created_at (str): When the snapshot was created
            id (str): Identifier of the snapshot on the compute plane Example: snap_abc123.
            name (str): Name of the snapshot, unique in its workspace Example: my-snapshot.
            status (str): Status of the snapshot (pending, ready, failed) Example: ready.
            workspace (str): Workspace owning the snapshot
            created_by (Union[Unset, str]): Who created the snapshot
            sandbox_name (Union[Unset, str]): Name of the source sandbox. Kept for compatibility, read source.name instead.
            source (Union[Unset, SandboxSnapshotSource]): The object a snapshot was captured from.
            spec (Union[Unset, SandboxSnapshotSpec]): The configuration a snapshot carries, so a sandbox or an application
                can be created from it once its source object is gone.
    """

    created_at: str
    id: str
    name: str
    status: str
    workspace: str
    created_by: Union[Unset, str] = UNSET
    sandbox_name: Union[Unset, str] = UNSET
    source: Union[Unset, "SandboxSnapshotSource"] = UNSET
    spec: Union[Unset, "SandboxSnapshotSpec"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        id = self.id

        name = self.name

        status = self.status

        workspace = self.workspace

        created_by = self.created_by

        sandbox_name = self.sandbox_name

        source: Union[Unset, dict[str, Any]] = UNSET
        if self.source and not isinstance(self.source, Unset) and not isinstance(self.source, dict):
            source = self.source.to_dict()
        elif self.source and isinstance(self.source, dict):
            source = self.source

        spec: Union[Unset, dict[str, Any]] = UNSET
        if self.spec and not isinstance(self.spec, Unset) and not isinstance(self.spec, dict):
            spec = self.spec.to_dict()
        elif self.spec and isinstance(self.spec, dict):
            spec = self.spec

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "id": id,
                "name": name,
                "status": status,
                "workspace": workspace,
            }
        )
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if sandbox_name is not UNSET:
            field_dict["sandboxName"] = sandbox_name
        if source is not UNSET:
            field_dict["source"] = source
        if spec is not UNSET:
            field_dict["spec"] = spec

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_snapshot_source import SandboxSnapshotSource
        from ..models.sandbox_snapshot_spec import SandboxSnapshotSpec

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt") if "createdAt" in d else d.pop("created_at")

        id = d.pop("id")

        name = d.pop("name")

        status = d.pop("status")

        workspace = d.pop("workspace")

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        sandbox_name = d.pop("sandboxName", d.pop("sandbox_name", UNSET))

        _source = d.pop("source", UNSET)
        source: Union[Unset, SandboxSnapshotSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = SandboxSnapshotSource.from_dict(_source)

        _spec = d.pop("spec", UNSET)
        spec: Union[Unset, SandboxSnapshotSpec]
        if isinstance(_spec, Unset):
            spec = UNSET
        else:
            spec = SandboxSnapshotSpec.from_dict(_spec)

        sandbox_snapshot = cls(
            created_at=created_at,
            id=id,
            name=name,
            status=status,
            workspace=workspace,
            created_by=created_by,
            sandbox_name=sandbox_name,
            source=source,
            spec=spec,
        )

        sandbox_snapshot.additional_properties = d
        return sandbox_snapshot

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
