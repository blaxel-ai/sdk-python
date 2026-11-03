from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationEndpointToken")


@_attrs_define
class IntegrationEndpointToken:
    """Integration endpoint token

    Attributes:
        received (str | Unset): Integration endpoint token received
        sent (str | Unset): Integration endpoint token sent
        total (str | Unset): Integration endpoint token total
    """

    received: str | Unset = UNSET
    sent: str | Unset = UNSET
    total: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        received = self.received

        sent = self.sent

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if received is not UNSET:
            field_dict["received"] = received
        if sent is not UNSET:
            field_dict["sent"] = sent
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        received = d.pop("received", UNSET)

        sent = d.pop("sent", UNSET)

        total = d.pop("total", UNSET)

        integration_endpoint_token = cls(
            received=received,
            sent=sent,
            total=total,
        )

        integration_endpoint_token.additional_properties = d
        return integration_endpoint_token

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
