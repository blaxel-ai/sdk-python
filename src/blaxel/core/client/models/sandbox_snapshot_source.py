from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_snapshot_source_kind import SandboxSnapshotSourceKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxSnapshotSource")


@_attrs_define
class SandboxSnapshotSource:
    """The object a snapshot was captured from.

    Attributes:
        name (str): Name of the object the snapshot was captured from
        deleted (Union[Unset, bool]): Whether the source object has since been deleted. The snapshot stays usable, the
            link is only kept for context.
        kind (Union[Unset, SandboxSnapshotSourceKind]): Kind of the object the snapshot was captured from. Defaults to
            sandbox, the only kind that can be captured today. Default: SandboxSnapshotSourceKind.SANDBOX. Example: sandbox.
    """

    name: str
    deleted: Union[Unset, bool] = UNSET
    kind: Union[Unset, SandboxSnapshotSourceKind] = SandboxSnapshotSourceKind.SANDBOX
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        deleted = self.deleted

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name")

        deleted = d.pop("deleted", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, SandboxSnapshotSourceKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = SandboxSnapshotSourceKind(_kind)

        sandbox_snapshot_source = cls(
            name=name,
            deleted=deleted,
            kind=kind,
        )

        sandbox_snapshot_source.additional_properties = d
        return sandbox_snapshot_source

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
