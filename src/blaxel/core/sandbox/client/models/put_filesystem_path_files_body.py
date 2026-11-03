from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PutFilesystemPathFilesBody")


@_attrs_define
class PutFilesystemPathFilesBody:
    """
    Attributes:
        file (File): File content
        permissions (str | Unset): Octal mode applied when the file is created (default 0644); an existing file keeps
            its mode Example: 0755.
        path (str | Unset): Ignored: the target is always the URL path
    """

    file: File
    permissions: str | Unset = UNSET
    path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        permissions = self.permissions

        path = self.path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        if not isinstance(self.permissions, Unset):
            files.append(("permissions", (None, str(self.permissions).encode(), "text/plain")))

        if not isinstance(self.path, Unset):
            files.append(("path", (None, str(self.path).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("file")))

        permissions = d.pop("permissions", UNSET)

        path = d.pop("path", UNSET)

        put_filesystem_path_files_body = cls(
            file=file,
            permissions=permissions,
            path=path,
        )

        put_filesystem_path_files_body.additional_properties = d
        return put_filesystem_path_files_body

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
