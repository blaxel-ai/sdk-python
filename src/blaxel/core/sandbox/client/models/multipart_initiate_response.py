from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MultipartInitiateResponse")


@_attrs_define
class MultipartInitiateResponse:
    """
    Attributes:
        path (Union[Unset, str]):  Example: /tmp/largefile.dat.
        upload_id (Union[Unset, str]):  Example: 550e8400-e29b-41d4-a716-446655440000.
    """

    path: Union[Unset, str] = UNSET
    upload_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        upload_id = self.upload_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if upload_id is not UNSET:
            field_dict["uploadId"] = upload_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        upload_id = d.pop("uploadId", d.pop("upload_id", UNSET))

        multipart_initiate_response = cls(
            path=path,
            upload_id=upload_id,
        )

        multipart_initiate_response.additional_properties = d
        return multipart_initiate_response

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
