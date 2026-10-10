from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filesystem_uploaded_part import FilesystemUploadedPart


T = TypeVar("T", bound="MultipartListPartsResponse")


@_attrs_define
class MultipartListPartsResponse:
    """
    Attributes:
        parts (Union[Unset, list['FilesystemUploadedPart']]):
        upload_id (Union[Unset, str]):  Example: 550e8400-e29b-41d4-a716-446655440000.
    """

    parts: Union[Unset, list["FilesystemUploadedPart"]] = UNSET
    upload_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parts, Unset):
            parts = []
            for parts_item_data in self.parts:
                if type(parts_item_data) is dict:
                    parts_item = parts_item_data
                else:
                    parts_item = parts_item_data.to_dict()
                parts.append(parts_item)

        upload_id = self.upload_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if parts is not UNSET:
            field_dict["parts"] = parts
        if upload_id is not UNSET:
            field_dict["uploadId"] = upload_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.filesystem_uploaded_part import FilesystemUploadedPart

        if not src_dict:
            return None
        d = src_dict.copy()
        parts = []
        _parts = d.pop("parts", UNSET)
        for parts_item_data in _parts or []:
            parts_item = FilesystemUploadedPart.from_dict(parts_item_data)

            parts.append(parts_item)

        upload_id = d.pop("uploadId", d.pop("upload_id", UNSET))

        multipart_list_parts_response = cls(
            parts=parts,
            upload_id=upload_id,
        )

        multipart_list_parts_response.additional_properties = d
        return multipart_list_parts_response

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
