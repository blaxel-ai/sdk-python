from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.egress_ip_spec_ip_family import EgressIPSpecIpFamily
from ..types import UNSET, Unset

T = TypeVar("T", bound="EgressIPSpec")


@_attrs_define
class EgressIPSpec:
    """Specification for an egress IP including IP family and the provisioned address

    Attributes:
        ip_family (EgressIPSpecIpFamily): IP address family, either IPv4 or IPv6 Default: EgressIPSpecIpFamily.IPV4.
            Example: IPv4.
        public_ip (Union[Unset, str]): Public IP address assigned to this egress IP (read-only, set after provisioning)
    """

    ip_family: EgressIPSpecIpFamily = EgressIPSpecIpFamily.IPV4
    public_ip: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip_family = self.ip_family.value

        public_ip = self.public_ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ipFamily": ip_family,
            }
        )
        if public_ip is not UNSET:
            field_dict["publicIp"] = public_ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        ip_family = EgressIPSpecIpFamily(
            d.pop("ipFamily") if "ipFamily" in d else d.pop("ip_family")
        )

        public_ip = d.pop("publicIp", d.pop("public_ip", UNSET))

        egress_ip_spec = cls(
            ip_family=ip_family,
            public_ip=public_ip,
        )

        egress_ip_spec.additional_properties = d
        return egress_ip_spec

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
