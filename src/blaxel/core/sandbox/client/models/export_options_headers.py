from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportOptionsHeaders")


@_attrs_define
class ExportOptionsHeaders:
    """Headers are sent with the upload request as given. A presigned URL only
    accepts the headers it was signed for, so these have to match what the
    caller signed: sending one that was not signed, or signing one that is not
    sent, is rejected as a signature mismatch. Typical use is a storage class,
    x-amz-storage-class: GLACIER_IR.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        export_options_headers = cls()

        export_options_headers.additional_properties = d
        return export_options_headers

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
