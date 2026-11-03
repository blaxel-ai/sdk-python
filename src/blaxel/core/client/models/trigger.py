from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

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
        configuration (TriggerConfiguration | Unset): Trigger configuration
        enabled (bool | Unset): Enable or disable the trigger (default: true) Example: True.
        id (str | Unset): Identifier of the trigger. Optional — the server auto-generates a unique id when one is not
            provided, and disambiguates duplicates within a resource. Example: trigger-1.
        type_ (TriggerType | Unset): The type of trigger, can be http or http-async Example: http.
    """

    configuration: TriggerConfiguration | Unset = UNSET
    enabled: bool | Unset = UNSET
    id: str | Unset = UNSET
    type_: TriggerType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configuration: dict[str, Any] | Unset = UNSET
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

        type_: str | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.trigger_configuration import TriggerConfiguration  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        _configuration = d.pop("configuration", UNSET)
        configuration: TriggerConfiguration | Unset
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = TriggerConfiguration.from_dict(_configuration)

        enabled = d.pop("enabled", UNSET)

        id = d.pop("id", UNSET)

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: TriggerType | Unset
        if isinstance(_type_, Unset) or _type_ == "":
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
