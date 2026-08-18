from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxSnapshot")


@_attrs_define
class SandboxSnapshot:
    """A point-in-time snapshot of a sandbox that can be used for forking into a new sandbox or application.

    Attributes:
        created_at (str): When the snapshot was created
        id (str): Unique snapshot identifier Example: snap_abc123.
        sandbox_name (str): Name of the source sandbox
        status (str): Status of the snapshot (pending, ready, failed) Example: ready.
        workspace (str): Workspace of the source sandbox
        created_by (Union[Unset, str]): Who created the snapshot
        name (Union[Unset, str]): Optional human-readable name for the snapshot Example: before-migration.
    """

    created_at: str
    id: str
    sandbox_name: str
    status: str
    workspace: str
    created_by: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        id = self.id

        sandbox_name = self.sandbox_name

        status = self.status

        workspace = self.workspace

        created_by = self.created_by

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "id": id,
                "sandboxName": sandbox_name,
                "status": status,
                "workspace": workspace,
            }
        )
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt") if "createdAt" in d else d.pop("created_at")

        id = d.pop("id")

        sandbox_name = d.pop("sandboxName") if "sandboxName" in d else d.pop("sandbox_name")

        status = d.pop("status")

        workspace = d.pop("workspace")

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        name = d.pop("name", UNSET)

        sandbox_snapshot = cls(
            created_at=created_at,
            id=id,
            sandbox_name=sandbox_name,
            status=status,
            workspace=workspace,
            created_by=created_by,
            name=name,
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
