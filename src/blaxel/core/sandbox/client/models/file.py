from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="File")


@_attrs_define
class File:
    """
    Attributes:
        group (str):
        last_modified (str):
        name (str):
        owner (str):
        path (str):
        permissions (str):
        size (int):
    """

    group: str
    last_modified: str
    name: str
    owner: str
    path: str
    permissions: str
    size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group = self.group

        last_modified = self.last_modified

        name = self.name

        owner = self.owner

        path = self.path

        permissions = self.permissions

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group": group,
                "lastModified": last_modified,
                "name": name,
                "owner": owner,
                "path": path,
                "permissions": permissions,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        group = d.pop("group")

        last_modified = d.pop("lastModified")

        name = d.pop("name")

        owner = d.pop("owner")

        path = d.pop("path")

        permissions = d.pop("permissions")

        size = d.pop("size")

        file = cls(
            group=group,
            last_modified=last_modified,
            name=name,
            owner=owner,
            path=path,
            permissions=permissions,
            size=size,
        )

        file.additional_properties = d
        return file

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
