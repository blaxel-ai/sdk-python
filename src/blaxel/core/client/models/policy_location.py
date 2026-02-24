from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_location_type import PolicyLocationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PolicyLocation")


@_attrs_define
class PolicyLocation:
    """Policy location

    Attributes:
        name (Union[Unset, str]): Policy location name Example: EU.
        type_ (Union[Unset, PolicyLocationType]): Policy location type Example: continent.
    """

    name: Union[Unset, str] = UNSET
    type_: Union[Unset, PolicyLocationType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: Union[Unset, PolicyLocationType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = PolicyLocationType(_type_)

        policy_location = cls(
            name=name,
            type_=type_,
        )

        policy_location.additional_properties = d
        return policy_location

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
