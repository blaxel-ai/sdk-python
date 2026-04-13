from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.egress_policy import EgressPolicy


T = TypeVar("T", bound="EgressConfig")


@_attrs_define
class EgressConfig:
    """Egress configuration for routing sandbox outbound traffic through a dedicated IP gateway

    Attributes:
        gateway (Union[Unset, str]): Name of the egress gateway to route traffic through. The gateway must exist in the
            default VPC. Example: egress-ip-gw-1.
        mode (Union[Unset, str]): Egress mode. Use 'dedicated' for a dedicated egress IP. Example: dedicated.
        policies (Union[Unset, list['EgressPolicy']]): Per-destination egress policies (not yet supported)
    """

    gateway: Union[Unset, str] = UNSET
    mode: Union[Unset, str] = UNSET
    policies: Union[Unset, list["EgressPolicy"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        gateway = self.gateway

        mode = self.mode

        policies: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = []
            for policies_item_data in self.policies:
                if type(policies_item_data) is dict:
                    policies_item = policies_item_data
                else:
                    policies_item = policies_item_data.to_dict()
                policies.append(policies_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if gateway is not UNSET:
            field_dict["gateway"] = gateway
        if mode is not UNSET:
            field_dict["mode"] = mode
        if policies is not UNSET:
            field_dict["policies"] = policies

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.egress_policy import EgressPolicy

        if not src_dict:
            return None
        d = src_dict.copy()
        gateway = d.pop("gateway", UNSET)

        mode = d.pop("mode", UNSET)

        policies = []
        _policies = d.pop("policies", UNSET)
        for policies_item_data in _policies or []:
            policies_item = EgressPolicy.from_dict(policies_item_data)

            policies.append(policies_item)

        egress_config = cls(
            gateway=gateway,
            mode=mode,
            policies=policies,
        )

        egress_config.additional_properties = d
        return egress_config

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
