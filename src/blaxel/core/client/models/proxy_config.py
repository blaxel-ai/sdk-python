from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.proxy_target import ProxyTarget


T = TypeVar("T", bound="ProxyConfig")


@_attrs_define
class ProxyConfig:
    """Proxy configuration for routing sandbox HTTP traffic through the platform proxy with MITM inspection and per-
    destination header/body injection

        Attributes:
            bypass (Union[Unset, list[str]]): Domains that bypass the proxy entirely via the NO_PROXY directive. Traffic to
                these destinations goes direct, not through the CONNECT tunnel. Supports wildcards. Note that localhost, private
                ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16), 169.254.169.254, .local and .internal are always bypassed by
                default. Example: ["*.s3.amazonaws.com"].
            routing (Union[Unset, list['ProxyTarget']]): Per-destination routing rules with header/body injection and
                secrets. Use destinations ["*"] for global rules that apply to all destinations.
    """

    bypass: Union[Unset, list[str]] = UNSET
    routing: Union[Unset, list["ProxyTarget"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        bypass: Union[Unset, list[str]] = UNSET
        if not isinstance(self.bypass, Unset):
            bypass = self.bypass

        routing: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.routing, Unset):
            routing = []
            for routing_item_data in self.routing:
                if type(routing_item_data) is dict:
                    routing_item = routing_item_data
                else:
                    routing_item = routing_item_data.to_dict()
                routing.append(routing_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bypass is not UNSET:
            field_dict["bypass"] = bypass
        if routing is not UNSET:
            field_dict["routing"] = routing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.proxy_target import ProxyTarget

        if not src_dict:
            return None
        d = src_dict.copy()
        bypass = cast(list[str], d.pop("bypass", UNSET))

        routing = []
        _routing = d.pop("routing", UNSET)
        for routing_item_data in _routing or []:
            routing_item = ProxyTarget.from_dict(routing_item_data)

            routing.append(routing_item)

        proxy_config = cls(
            bypass=bypass,
            routing=routing,
        )

        proxy_config.additional_properties = d
        return proxy_config

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
