from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trigger_type import TriggerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trigger_configuration import TriggerConfiguration


T = TypeVar("T", bound="Trigger")


@_attrs_define
class Trigger:
    """Trigger configuration

    Attributes:
        configuration (Union[Unset, TriggerConfiguration]): Trigger configuration
        enabled (Union[Unset, bool]): Enable or disable the trigger (default: true) Example: True.
        id (Union[Unset, str]): The id of the trigger Example: trigger-1.
        type_ (Union[Unset, TriggerType]): The type of trigger, can be http or http-async Example: http.
    """

    configuration: Union[Unset, "TriggerConfiguration"] = UNSET
    enabled: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    type_: Union[Unset, TriggerType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configuration: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.configuration
            and not isinstance(self.configuration, Unset)
            and not isinstance(self.configuration, dict)
        ):
            configuration = self.configuration.to_dict()
        elif self.configuration and isinstance(self.configuration, dict):
            configuration = self.configuration

        enabled = self.enabled

        id = self.id

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.trigger_configuration import TriggerConfiguration

        if not src_dict:
            return None
        d = src_dict.copy()
        _configuration = d.pop("configuration", UNSET)
        configuration: Union[Unset, TriggerConfiguration]
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = TriggerConfiguration.from_dict(_configuration)

        enabled = d.pop("enabled", UNSET)

        id = d.pop("id", UNSET)

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: Union[Unset, TriggerType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TriggerType(_type_)

        trigger = cls(
            configuration=configuration,
            enabled=enabled,
            id=id,
            type_=type_,
        )

        trigger.additional_properties = d
        return trigger

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
