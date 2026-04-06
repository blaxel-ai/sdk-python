from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EgressPolicy")


@_attrs_define
class EgressPolicy:
    """Egress policy routing specific destinations through dedicated or shared gateways (not yet supported)

    Attributes:
        destinations (Union[Unset, list[str]]): Destination domains or IPs this policy applies to Example:
            ["api.stripe.com"].
        mode (Union[Unset, str]): Egress mode for these destinations (dedicated or shared) Example: dedicated.
        name (Union[Unset, str]): Name of this egress policy Example: payment-apis.
    """

    destinations: Union[Unset, list[str]] = UNSET
    mode: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destinations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = self.destinations

        mode = self.mode

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if destinations is not UNSET:
            field_dict["destinations"] = destinations
        if mode is not UNSET:
            field_dict["mode"] = mode
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        destinations = cast(list[str], d.pop("destinations", UNSET))

        mode = d.pop("mode", UNSET)

        name = d.pop("name", UNSET)

        egress_policy = cls(
            destinations=destinations,
            mode=mode,
            name=name,
        )

        egress_policy.additional_properties = d
        return egress_policy

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
