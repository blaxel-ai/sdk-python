from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.egress_config import EgressConfig
    from ..models.firewall_config import FirewallConfig
    from ..models.proxy_config import ProxyConfig


T = TypeVar("T", bound="SandboxNetwork")


@_attrs_define
class SandboxNetwork:
    """Network configuration for a sandbox including subnet, firewall rulesets, domain filtering, egress IP binding, and
    proxy settings

        Attributes:
            allowed_domains (Union[Unset, list[str]]): Deprecated: use proxy.allowedDomains instead. List of allowed
                external domains (allowlist). Kept for backward compatibility. Example: ["api.stripe.com", "api.openai.com",
                "*.s3.amazonaws.com"].
            egress (Union[Unset, EgressConfig]): Egress configuration for routing sandbox outbound traffic through a
                dedicated IP gateway
            firewall (Union[Unset, FirewallConfig]): Firewall configuration specifying which network lockdown rulesets to
                apply. Valid rulesets are "default" (no-op), "proxy" (restrict egress to proxy), and "dedicated-ip" (restrict
                egress to dedicated IP gateway).
            forbidden_domains (Union[Unset, list[str]]): Deprecated: use proxy.forbiddenDomains instead. List of forbidden
                external domains (denylist). Kept for backward compatibility. Example: ["*.malware.com", "evil.example.org"].
            proxy (Union[Unset, ProxyConfig]): Proxy configuration for routing sandbox HTTP traffic through the platform
                proxy with MITM inspection and per-destination header/body injection
            subnet (Union[Unset, str]): Subnet name for the sandbox. Takes priority over any subnet derived from egress
                config. Defaults to "default" when absent. Example: default.
    """

    allowed_domains: Union[Unset, list[str]] = UNSET
    egress: Union[Unset, "EgressConfig"] = UNSET
    firewall: Union[Unset, "FirewallConfig"] = UNSET
    forbidden_domains: Union[Unset, list[str]] = UNSET
    proxy: Union[Unset, "ProxyConfig"] = UNSET
    subnet: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        allowed_domains: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_domains, Unset):
            allowed_domains = self.allowed_domains

        egress: Union[Unset, dict[str, Any]] = UNSET
        if self.egress and not isinstance(self.egress, Unset) and not isinstance(self.egress, dict):
            egress = self.egress.to_dict()
        elif self.egress and isinstance(self.egress, dict):
            egress = self.egress

        firewall: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.firewall
            and not isinstance(self.firewall, Unset)
            and not isinstance(self.firewall, dict)
        ):
            firewall = self.firewall.to_dict()
        elif self.firewall and isinstance(self.firewall, dict):
            firewall = self.firewall

        forbidden_domains: Union[Unset, list[str]] = UNSET
        if not isinstance(self.forbidden_domains, Unset):
            forbidden_domains = self.forbidden_domains

        proxy: Union[Unset, dict[str, Any]] = UNSET
        if self.proxy and not isinstance(self.proxy, Unset) and not isinstance(self.proxy, dict):
            proxy = self.proxy.to_dict()
        elif self.proxy and isinstance(self.proxy, dict):
            proxy = self.proxy

        subnet = self.subnet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains
        if egress is not UNSET:
            field_dict["egress"] = egress
        if firewall is not UNSET:
            field_dict["firewall"] = firewall
        if forbidden_domains is not UNSET:
            field_dict["forbiddenDomains"] = forbidden_domains
        if proxy is not UNSET:
            field_dict["proxy"] = proxy
        if subnet is not UNSET:
            field_dict["subnet"] = subnet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.egress_config import EgressConfig
        from ..models.firewall_config import FirewallConfig
        from ..models.proxy_config import ProxyConfig

        if not src_dict:
            return None
        d = src_dict.copy()
        allowed_domains = cast(list[str], d.pop("allowedDomains", d.pop("allowed_domains", UNSET)))

        _egress = d.pop("egress", UNSET)
        egress: Union[Unset, EgressConfig]
        if isinstance(_egress, Unset):
            egress = UNSET
        else:
            egress = EgressConfig.from_dict(_egress)

        _firewall = d.pop("firewall", UNSET)
        firewall: Union[Unset, FirewallConfig]
        if isinstance(_firewall, Unset):
            firewall = UNSET
        else:
            firewall = FirewallConfig.from_dict(_firewall)

        forbidden_domains = cast(
            list[str], d.pop("forbiddenDomains", d.pop("forbidden_domains", UNSET))
        )

        _proxy = d.pop("proxy", UNSET)
        proxy: Union[Unset, ProxyConfig]
        if isinstance(_proxy, Unset):
            proxy = UNSET
        else:
            proxy = ProxyConfig.from_dict(_proxy)

        subnet = d.pop("subnet", UNSET)

        sandbox_network = cls(
            allowed_domains=allowed_domains,
            egress=egress,
            firewall=firewall,
            forbidden_domains=forbidden_domains,
            proxy=proxy,
            subnet=subnet,
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
