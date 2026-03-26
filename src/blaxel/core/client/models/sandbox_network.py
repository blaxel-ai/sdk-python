from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.egress_config import EgressConfig
    from ..models.proxy_config import ProxyConfig


T = TypeVar("T", bound="SandboxNetwork")


@_attrs_define
class SandboxNetwork:
    """Network configuration for a sandbox including domain filtering, egress IP binding, and proxy settings

    Attributes:
        allowed_domains (Union[Unset, list[str]]): List of allowed external domains (allowlist). When set, only these
            domains are reachable. Supports wildcards (e.g. *.s3.amazonaws.com). Example: ["api.stripe.com",
            "api.openai.com", "*.s3.amazonaws.com"].
        egress (Union[Unset, EgressConfig]): Egress configuration for routing sandbox outbound traffic through a
            dedicated IP gateway
        forbidden_domains (Union[Unset, list[str]]): List of forbidden external domains (denylist). When set, all
            domains except these are reachable. Supports wildcards (e.g. *.malware.com). If both allowedDomains and
            forbiddenDomains are set, allowedDomains takes precedence. Example: ["*.malware.com", "evil.example.org"].
        proxy (Union[Unset, ProxyConfig]): Proxy configuration for routing sandbox HTTP traffic through the platform
            proxy with MITM inspection and per-destination header/body injection
    """

    allowed_domains: Union[Unset, list[str]] = UNSET
    egress: Union[Unset, "EgressConfig"] = UNSET
    forbidden_domains: Union[Unset, list[str]] = UNSET
    proxy: Union[Unset, "ProxyConfig"] = UNSET
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

        forbidden_domains: Union[Unset, list[str]] = UNSET
        if not isinstance(self.forbidden_domains, Unset):
            forbidden_domains = self.forbidden_domains

        proxy: Union[Unset, dict[str, Any]] = UNSET
        if self.proxy and not isinstance(self.proxy, Unset) and not isinstance(self.proxy, dict):
            proxy = self.proxy.to_dict()
        elif self.proxy and isinstance(self.proxy, dict):
            proxy = self.proxy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains
        if egress is not UNSET:
            field_dict["egress"] = egress
        if forbidden_domains is not UNSET:
            field_dict["forbiddenDomains"] = forbidden_domains
        if proxy is not UNSET:
            field_dict["proxy"] = proxy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.egress_config import EgressConfig
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

        forbidden_domains = cast(
            list[str], d.pop("forbiddenDomains", d.pop("forbidden_domains", UNSET))
        )

        _proxy = d.pop("proxy", UNSET)
        proxy: Union[Unset, ProxyConfig]
        if isinstance(_proxy, Unset):
            proxy = UNSET
        else:
            proxy = ProxyConfig.from_dict(_proxy)

        sandbox_network = cls(
            allowed_domains=allowed_domains,
            egress=egress,
            forbidden_domains=forbidden_domains,
            proxy=proxy,
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
