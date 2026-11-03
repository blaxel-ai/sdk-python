from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileRequest")


@_attrs_define
class FileRequest:
    """
    Attributes:
        content (str | Unset):  Example: file contents here.
        is_directory (bool | Unset):  Example: False.
        permissions (str | Unset):  Example: 0644.
    """

    content: str | Unset = UNSET
    is_directory: bool | Unset = UNSET
    permissions: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        is_directory = self.is_directory

        permissions = self.permissions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if is_directory is not UNSET:
            field_dict["isDirectory"] = is_directory
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        is_directory = d.pop("isDirectory", d.pop("is_directory", UNSET))

        permissions = d.pop("permissions", UNSET)

        file_request = cls(
            content=content,
            is_directory=is_directory,
            permissions=permissions,
        )

        file_request.additional_properties = d
        return file_request

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
