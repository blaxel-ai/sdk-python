from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.filesystem_uploaded_part import FilesystemUploadedPart


T = TypeVar("T", bound="FilesystemMultipartUploadParts")


@_attrs_define
class FilesystemMultipartUploadParts:
    """ """

    additional_properties: dict[str, "FilesystemUploadedPart"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if type(prop) is dict:
                field_dict[prop_name] = prop
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.filesystem_uploaded_part import FilesystemUploadedPart

        if not src_dict:
            return None
        d = src_dict.copy()
        filesystem_multipart_upload_parts = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = FilesystemUploadedPart.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        filesystem_multipart_upload_parts.additional_properties = additional_properties
        return filesystem_multipart_upload_parts

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "FilesystemUploadedPart":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "FilesystemUploadedPart") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
