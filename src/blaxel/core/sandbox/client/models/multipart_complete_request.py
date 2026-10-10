from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.multipart_part_info import MultipartPartInfo


T = TypeVar("T", bound="MultipartCompleteRequest")


@_attrs_define
class MultipartCompleteRequest:
    """
    Attributes:
        parts (Union[Unset, list['MultipartPartInfo']]):
    """

    parts: Union[Unset, list["MultipartPartInfo"]] = UNSET
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if parts is not UNSET:
            field_dict["parts"] = parts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.multipart_part_info import MultipartPartInfo

        if not src_dict:
            return None
        d = src_dict.copy()
        parts = []
        _parts = d.pop("parts", UNSET)
        for parts_item_data in _parts or []:
            parts_item = MultipartPartInfo.from_dict(parts_item_data)

            parts.append(parts_item)

        multipart_complete_request = cls(
            parts=parts,
        )

        multipart_complete_request.additional_properties = d
        return multipart_complete_request

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
