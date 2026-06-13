from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FirewallConfig")


@_attrs_define
class FirewallConfig:
    """Firewall configuration specifying which network lockdown rulesets to apply. Valid rulesets are "default" (no-op),
    "proxy" (restrict egress to proxy), and "dedicated-ip" (restrict egress to dedicated IP gateway).

        Attributes:
            rulesets (Union[Unset, list[str]]): List of firewall rulesets to apply. Valid values: "default" (no-op), "proxy"
                (restrict egress to proxy), "dedicated-ip" (restrict egress to dedicated IP gateway). Example: ["proxy"].
    """

    rulesets: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rulesets: Union[Unset, list[str]] = UNSET
        if not isinstance(self.rulesets, Unset):
            rulesets = self.rulesets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rulesets is not UNSET:
            field_dict["rulesets"] = rulesets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        rulesets = cast(list[str], d.pop("rulesets", UNSET))

        firewall_config = cls(
            rulesets=rulesets,
        )

        firewall_config.additional_properties = d
        return firewall_config

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
