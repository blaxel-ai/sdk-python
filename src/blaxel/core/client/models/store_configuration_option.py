from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StoreConfigurationOption")


@_attrs_define
class StoreConfigurationOption:
    """Store configuration options for a select type configuration

    Attributes:
        if_ (Union[Unset, str]): Conditional rendering for the configuration option, example: provider === 'openai'
        label (Union[Unset, str]): Store configuration option label
        value (Union[Unset, str]): Store configuration option value
    """

    if_: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if_ = self.if_

        label = self.label

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if if_ is not UNSET:
            field_dict["if"] = if_
        if label is not UNSET:
            field_dict["label"] = label
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        if_ = d.pop("if", UNSET)

        label = d.pop("label", UNSET)

        value = d.pop("value", UNSET)

        store_configuration_option = cls(
            if_=if_,
            label=label,
            value=value,
        )

        store_configuration_option.additional_properties = d
        return store_configuration_option

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
