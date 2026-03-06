from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SandboxNetwork")


@_attrs_define
class SandboxNetwork:
    """Network configuration for a sandbox including egress IP binding. All three fields (vpcName, egressGatewayName,
    egressIpName) must be specified together to assign a dedicated IP.

        Attributes:
            egress_gateway_name (str): Name of the egress gateway in the VPC. Must be specified together with vpcName and
                egressIpName. Example: my-egress-gateway.
            vpc_name (str): Name of the VPC where the egress gateway is provisioned. Must be specified together with
                egressGatewayName and egressIpName. Example: my-vpc.
    """

    egress_gateway_name: str
    vpc_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        egress_gateway_name = self.egress_gateway_name

        vpc_name = self.vpc_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "egressGatewayName": egress_gateway_name,
                "vpcName": vpc_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        egress_gateway_name = (
            d.pop("egressGatewayName") if "egressGatewayName" in d else d.pop("egress_gateway_name")
        )

        vpc_name = d.pop("vpcName") if "vpcName" in d else d.pop("vpc_name")

        sandbox_network = cls(
            egress_gateway_name=egress_gateway_name,
            vpc_name=vpc_name,
        )

        sandbox_network.additional_properties = d
        return sandbox_network

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
