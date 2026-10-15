from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.archive_change_kind import ArchiveChangeKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArchiveChange")


@_attrs_define
class ArchiveChange:
    """
    Attributes:
        kind (ArchiveChangeKind):
        path (str): Path is relative to the root, without a leading slash. Example: usr/bin/curl.
        size (Union[Unset, int]): Size is the file content size in bytes, 0 for anything but a regular file. Example:
            256216.
    """

    kind: ArchiveChangeKind
    path: str
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        path = self.path

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
            }
        )
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        kind = ArchiveChangeKind(d.pop("kind"))

        path = d.pop("path")

        size = d.pop("size", UNSET)

        archive_change = cls(
            kind=kind,
            path=path,
            size=size,
        )

        archive_change.additional_properties = d
        return archive_change

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
