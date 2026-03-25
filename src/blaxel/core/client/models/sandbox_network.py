from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxNetwork")


@_attrs_define
class SandboxNetwork:
    """Network configuration for a sandbox including egress IP binding, proxy routing, and firewall rules.

    Attributes:
        egress_gateway_name (Union[Unset, str]): Name of the egress gateway in the VPC.
            Must be specified together with vpcName. Example: my-egress-gateway.
        vpc_name (Union[Unset, str]): Name of the VPC where the egress gateway is provisioned.
            Must be specified together with egressGatewayName. Example: my-vpc.
    """

    egress_gateway_name: Union[Unset, str] = UNSET
    vpc_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if not isinstance(self.egress_gateway_name, Unset):
            field_dict["egressGatewayName"] = self.egress_gateway_name
        if not isinstance(self.vpc_name, Unset):
            field_dict["vpcName"] = self.vpc_name
        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()

        egress_gateway_name: Union[Unset, str] = UNSET
        if "egressGatewayName" in d:
            egress_gateway_name = d.pop("egressGatewayName")
        elif "egress_gateway_name" in d:
            egress_gateway_name = d.pop("egress_gateway_name")

        vpc_name: Union[Unset, str] = UNSET
        if "vpcName" in d:
            vpc_name = d.pop("vpcName")
        elif "vpc_name" in d:
            vpc_name = d.pop("vpc_name")

        sandbox_network = cls(
            egress_gateway_name=egress_gateway_name,
            vpc_name=vpc_name,
        )

        sandbox_network.additional_properties = d
        return sandbox_network

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def get(self, key: str, default: Any = None) -> Any:
        return self.additional_properties.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
