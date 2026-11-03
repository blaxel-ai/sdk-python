from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MultipartUploadPartResponse")


@_attrs_define
class MultipartUploadPartResponse:
    """
    Attributes:
        etag (str | Unset):  Example: 5d41402abc4b2a76b9719d911017c592.
        part_number (int | Unset):  Example: 1.
        size (int | Unset):  Example: 5242880.
    """

    etag: str | Unset = UNSET
    part_number: int | Unset = UNSET
    size: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        etag = self.etag

        part_number = self.part_number

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if etag is not UNSET:
            field_dict["etag"] = etag
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        etag = d.pop("etag", UNSET)

        part_number = d.pop("partNumber", d.pop("part_number", UNSET))

        size = d.pop("size", UNSET)

        multipart_upload_part_response = cls(
            etag=etag,
            part_number=part_number,
            size=size,
        )

        multipart_upload_part_response.additional_properties = d
        return multipart_upload_part_response

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
