from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LiteVolumeMetadata")


@_attrs_define
class LiteVolumeMetadata:
    """Compact metadata for a Volume, returned in listing responses.

    Attributes:
        created_at (Union[Unset, str]):
        display_name (Union[Unset, str]):
        name (Union[Unset, str]):
        updated_at (Union[Unset, str]):
    """

    created_at: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        display_name = self.display_name

        name = self.name

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if name is not UNSET:
            field_dict["name"] = name
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        name = d.pop("name", UNSET)

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        lite_volume_metadata = cls(
            created_at=created_at,
            display_name=display_name,
            name=name,
            updated_at=updated_at,
        )

        lite_volume_metadata.additional_properties = d
        return lite_volume_metadata

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
