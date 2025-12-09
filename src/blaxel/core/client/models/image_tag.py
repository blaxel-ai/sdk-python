from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageTag")


@_attrs_define
class ImageTag:
    """
    Attributes:
        created_at (Union[Unset, str]): The date and time when the tag was created.
        name (Union[Unset, str]): The name of the tag.
        size (Union[Unset, int]): The size of the image in bytes.
        updated_at (Union[Unset, str]): The date and time when the tag was last updated.
    """

    created_at: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    updated_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        name = self.name

        size = self.size

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        image_tag = cls(
            created_at=created_at,
            name=name,
            size=size,
            updated_at=updated_at,
        )

        image_tag.additional_properties = d
        return image_tag

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
