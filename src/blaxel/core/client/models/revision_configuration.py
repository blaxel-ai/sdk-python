from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RevisionConfiguration")


@_attrs_define
class RevisionConfiguration:
    """Revision configuration

    Attributes:
        active (Union[Unset, str]): Active revision id Example: rev-abc123.
        canary (Union[Unset, str]): Canary revision id
        canary_percent (Union[Unset, int]): Canary revision percent Example: 10.
        sticky_session_ttl (Union[Unset, int]): Sticky session TTL in seconds (0 = disabled)
        traffic (Union[Unset, int]): Traffic percentage Example: 100.
    """

    active: Union[Unset, str] = UNSET
    canary: Union[Unset, str] = UNSET
    canary_percent: Union[Unset, int] = UNSET
    sticky_session_ttl: Union[Unset, int] = UNSET
    traffic: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active = self.active

        canary = self.canary

        canary_percent = self.canary_percent

        sticky_session_ttl = self.sticky_session_ttl

        traffic = self.traffic

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if canary is not UNSET:
            field_dict["canary"] = canary
        if canary_percent is not UNSET:
            field_dict["canaryPercent"] = canary_percent
        if sticky_session_ttl is not UNSET:
            field_dict["stickySessionTtl"] = sticky_session_ttl
        if traffic is not UNSET:
            field_dict["traffic"] = traffic

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        active = d.pop("active", UNSET)

        canary = d.pop("canary", UNSET)

        canary_percent = d.pop("canaryPercent", d.pop("canary_percent", UNSET))

        sticky_session_ttl = d.pop("stickySessionTtl", d.pop("sticky_session_ttl", UNSET))

        traffic = d.pop("traffic", UNSET)

        revision_configuration = cls(
            active=active,
            canary=canary,
            canary_percent=canary_percent,
            sticky_session_ttl=sticky_session_ttl,
            traffic=traffic,
        )

        revision_configuration.additional_properties = d
        return revision_configuration

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
