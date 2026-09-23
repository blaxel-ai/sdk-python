from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageSummarySpec")


@_attrs_define
class ImageSummarySpec:
    """
    Attributes:
        size (Union[Unset, int]):
        tag_count (Union[Unset, int]):
    """

    size: Union[Unset, int] = UNSET
    tag_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        size = self.size

        tag_count = self.tag_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if tag_count is not UNSET:
            field_dict["tagCount"] = tag_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        tag_count = d.pop("tagCount", d.pop("tag_count", UNSET))

        image_summary_spec = cls(
            size=size,
            tag_count=tag_count,
        )

        image_summary_spec.additional_properties = d
        return image_summary_spec

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
