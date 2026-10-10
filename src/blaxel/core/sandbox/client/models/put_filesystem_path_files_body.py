from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PutFilesystemPathFilesBody")


@_attrs_define
class PutFilesystemPathFilesBody:
    """
    Attributes:
        file (File): File content
        permissions (Union[Unset, str]): Octal mode applied when the file is created (default 0644); an existing file
            keeps its mode Example: 0755.
        path (Union[Unset, str]): Ignored: the target is always the URL path
    """

    file: File
    permissions: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
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

    def to_multipart(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        permissions = (
            self.permissions
            if isinstance(self.permissions, Unset)
            else (None, str(self.permissions).encode(), "text/plain")
        )

        path = (
            self.path
            if isinstance(self.path, Unset)
            else (None, str(self.path).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

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

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
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
