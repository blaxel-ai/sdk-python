from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="File")


@_attrs_define
class File:
    """
    Attributes:
        group (Union[Unset, str]):
        last_modified (Union[Unset, str]):
        owner (Union[Unset, str]):
        path (Union[Unset, str]):
        permissions (Union[Unset, str]):
        size (Union[Unset, int]):
    """

    group: Union[Unset, str] = UNSET
    last_modified: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    permissions: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group = self.group

        last_modified = self.last_modified

        owner = self.owner

        path = self.path

        permissions = self.permissions

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if group is not UNSET:
            field_dict["group"] = group
        if last_modified is not UNSET:
            field_dict["lastModified"] = last_modified
        if owner is not UNSET:
            field_dict["owner"] = owner
        if path is not UNSET:
            field_dict["path"] = path
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        group = d.pop("group", UNSET)

        last_modified = d.pop("lastModified", UNSET)

        owner = d.pop("owner", UNSET)

        path = d.pop("path", UNSET)

        permissions = d.pop("permissions", UNSET)

        size = d.pop("size", UNSET)

        file = cls(
            group=group,
            last_modified=last_modified,
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
