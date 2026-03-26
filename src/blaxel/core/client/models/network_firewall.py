from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetworkFirewall")


@_attrs_define
class NetworkFirewall:
    """Firewall configuration restricting which external domains the sandbox can access

    Attributes:
        allowed_domains (Union[Unset, list[str]]): List of allowed external domains. Supports wildcards (e.g.
            *.s3.amazonaws.com). Example: ["api.stripe.com", "api.openai.com", "*.s3.amazonaws.com"].
    """

    allowed_domains: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed_domains: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_domains, Unset):
            allowed_domains = self.allowed_domains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        allowed_domains = cast(list[str], d.pop("allowedDomains", d.pop("allowed_domains", UNSET)))

        network_firewall = cls(
            allowed_domains=allowed_domains,
        )

        network_firewall.additional_properties = d
        return network_firewall

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
