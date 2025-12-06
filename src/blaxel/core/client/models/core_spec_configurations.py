from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.spec_configuration import SpecConfiguration


T = TypeVar("T", bound="CoreSpecConfigurations")


@_attrs_define
class CoreSpecConfigurations:
    """Optional configurations for the object

    Attributes:
        key (Union[Unset, SpecConfiguration]): Configuration, this is a key value storage. In your object you can
            retrieve the value with config[key]
    """

    key: Union[Unset, "SpecConfiguration"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key: Union[Unset, dict[str, Any]] = UNSET
        if self.key and not isinstance(self.key, Unset) and not isinstance(self.key, dict):
            key = self.key.to_dict()
        elif self.key and isinstance(self.key, dict):
            key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.spec_configuration import SpecConfiguration

        if not src_dict:
            return None
        d = src_dict.copy()
        _key = d.pop("key", UNSET)
        key: Union[Unset, SpecConfiguration]
        if isinstance(_key, Unset):
            key = UNSET
        else:
            key = SpecConfiguration.from_dict(_key)

        core_spec_configurations = cls(
            key=key,
        )

        core_spec_configurations.additional_properties = d
        return core_spec_configurations

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
