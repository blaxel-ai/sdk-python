from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filesystem_multipart_upload_parts import FilesystemMultipartUploadParts


T = TypeVar("T", bound="FilesystemMultipartUpload")


@_attrs_define
class FilesystemMultipartUpload:
    """
    Attributes:
        initiated_at (str | Unset):
        parts (FilesystemMultipartUploadParts | Unset):
        path (str | Unset):  Example: /tmp/largefile.dat.
        permissions (int | Unset):  Example: 420.
        upload_id (str | Unset):  Example: 550e8400-e29b-41d4-a716-446655440000.
    """

    initiated_at: str | Unset = UNSET
    parts: FilesystemMultipartUploadParts | Unset = UNSET
    path: str | Unset = UNSET
    permissions: int | Unset = UNSET
    upload_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        initiated_at = self.initiated_at

        parts: dict[str, Any] | Unset = UNSET
        if self.parts and not isinstance(self.parts, Unset) and not isinstance(self.parts, dict):
            parts = self.parts.to_dict()
        elif self.parts and isinstance(self.parts, dict):
            parts = self.parts

        path = self.path

        permissions = self.permissions

        upload_id = self.upload_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if initiated_at is not UNSET:
            field_dict["initiatedAt"] = initiated_at
        if parts is not UNSET:
            field_dict["parts"] = parts
        if path is not UNSET:
            field_dict["path"] = path
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if upload_id is not UNSET:
            field_dict["uploadId"] = upload_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.filesystem_multipart_upload_parts import (
            FilesystemMultipartUploadParts,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        initiated_at = d.pop("initiatedAt", d.pop("initiated_at", UNSET))

        _parts = d.pop("parts", UNSET)
        parts: FilesystemMultipartUploadParts | Unset
        if isinstance(_parts, Unset):
            parts = UNSET
        else:
            parts = FilesystemMultipartUploadParts.from_dict(_parts)

        path = d.pop("path", UNSET)

        permissions = d.pop("permissions", UNSET)

        upload_id = d.pop("uploadId", d.pop("upload_id", UNSET))

        filesystem_multipart_upload = cls(
            initiated_at=initiated_at,
            parts=parts,
            path=path,
            permissions=permissions,
            upload_id=upload_id,
        )

        filesystem_multipart_upload.additional_properties = d
        return filesystem_multipart_upload

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
