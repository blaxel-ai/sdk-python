from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppRevisionConfiguration")


@_attrs_define
class AppRevisionConfiguration:
    """Routing configuration controlling which revision is active and canary traffic splitting

    Attributes:
        active (str | Unset): Active revision id
        canary (str | Unset): Canary revision id
        canary_percent (int | Unset): Canary revision percent (0-100) Example: 10.
        sticky_session_ttl (int | Unset): Sticky session TTL in seconds (0 = disabled) Example: 0.
        traffic (int | Unset): Traffic percentage for deployment Example: 100.
    """

    active: str | Unset = UNSET
    canary: str | Unset = UNSET
    canary_percent: int | Unset = UNSET
    sticky_session_ttl: int | Unset = UNSET
    traffic: int | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        active = d.pop("active", UNSET)

        canary = d.pop("canary", UNSET)

        canary_percent = d.pop("canaryPercent", d.pop("canary_percent", UNSET))

        sticky_session_ttl = d.pop("stickySessionTtl", d.pop("sticky_session_ttl", UNSET))

        traffic = d.pop("traffic", UNSET)

        app_revision_configuration = cls(
            active=active,
            canary=canary,
            canary_percent=canary_percent,
            sticky_session_ttl=sticky_session_ttl,
            traffic=traffic,
        )

        app_revision_configuration.additional_properties = d
        return app_revision_configuration

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
