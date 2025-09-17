from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpirationPolicy")


@_attrs_define
class ExpirationPolicy:
    """Expiration policy for sandbox lifecycle management

    Attributes:
        action (Union[Unset, str]): Action to take when policy is triggered
        type_ (Union[Unset, str]): Type of expiration policy
        value (Union[Unset, str]): Duration value (e.g., '1h', '24h', '7d')
    """

    action: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        type_ = self.type_

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        action = d.pop("action", UNSET)

        type_ = d.pop("type", UNSET)

        value = d.pop("value", UNSET)

        expiration_policy = cls(
            action=action,
            type_=type_,
            value=value,
        )

        expiration_policy.additional_properties = d
        return expiration_policy

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
