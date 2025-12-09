from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FilesystemUploadedPart")


@_attrs_define
class FilesystemUploadedPart:
    """
    Attributes:
        etag (Union[Unset, str]):  Example: 5d41402abc4b2a76b9719d911017c592.
        part_number (Union[Unset, int]):  Example: 1.
        size (Union[Unset, int]):  Example: 5242880.
        uploaded_at (Union[Unset, str]):
    """

    etag: Union[Unset, str] = UNSET
    part_number: Union[Unset, int] = UNSET
    size: Union[Unset, int] = UNSET
    uploaded_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        etag = self.etag

        part_number = self.part_number

        size = self.size

        uploaded_at = self.uploaded_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if etag is not UNSET:
            field_dict["etag"] = etag
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if size is not UNSET:
            field_dict["size"] = size
        if uploaded_at is not UNSET:
            field_dict["uploadedAt"] = uploaded_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        etag = d.pop("etag", UNSET)

        part_number = d.pop("partNumber", d.pop("part_number", UNSET))

        size = d.pop("size", UNSET)

        uploaded_at = d.pop("uploadedAt", d.pop("uploaded_at", UNSET))

        filesystem_uploaded_part = cls(
            etag=etag,
            part_number=part_number,
            size=size,
            uploaded_at=uploaded_at,
        )

        filesystem_uploaded_part.additional_properties = d
        return filesystem_uploaded_part

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
