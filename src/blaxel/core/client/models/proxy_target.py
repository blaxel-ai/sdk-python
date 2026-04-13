from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.proxy_target_body import ProxyTargetBody
    from ..models.proxy_target_headers import ProxyTargetHeaders
    from ..models.proxy_target_secrets import ProxyTargetSecrets


T = TypeVar("T", bound="ProxyTarget")


@_attrs_define
class ProxyTarget:
    """Routing rule that injects headers and body fields into requests matching the given destinations. Use destinations
    ["*"] for a global rule that applies to all proxied traffic.

        Attributes:
            body (Union[Unset, ProxyTargetBody]): Body fields to inject into matching requests. Values may contain
                {{SECRET:name}} references resolved from this rule's secrets. Example: {"api_key": "{{SECRET:stripe-key}}"}.
            destinations (Union[Unset, list[str]]): Destination domains this rule applies to. Use ["*"] for a global rule
                that matches all destinations. Example: ["api.stripe.com"].
            headers (Union[Unset, ProxyTargetHeaders]): Headers to inject into matching requests. Values may contain
                {{SECRET:name}} references resolved from this rule's secrets. Example: {"Authorization": "Bearer
                {{SECRET:stripe-key}}"}.
            secrets (Union[Unset, ProxyTargetSecrets]): Named secret values for this routing rule, referenced in
                headers/body via {{SECRET:name}}. Stored encrypted at rest. Write-only: never returned in API responses.
                Example: {"stripe-key": "sk-live-abc123..."}.
    """

    body: Union[Unset, "ProxyTargetBody"] = UNSET
    destinations: Union[Unset, list[str]] = UNSET
    headers: Union[Unset, "ProxyTargetHeaders"] = UNSET
    secrets: Union[Unset, "ProxyTargetSecrets"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        body: Union[Unset, dict[str, Any]] = UNSET
        if self.body and not isinstance(self.body, Unset) and not isinstance(self.body, dict):
            body = self.body.to_dict()
        elif self.body and isinstance(self.body, dict):
            body = self.body

        destinations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.destinations, Unset):
            destinations = self.destinations

        headers: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.headers
            and not isinstance(self.headers, Unset)
            and not isinstance(self.headers, dict)
        ):
            headers = self.headers.to_dict()
        elif self.headers and isinstance(self.headers, dict):
            headers = self.headers

        secrets: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.secrets
            and not isinstance(self.secrets, Unset)
            and not isinstance(self.secrets, dict)
        ):
            secrets = self.secrets.to_dict()
        elif self.secrets and isinstance(self.secrets, dict):
            secrets = self.secrets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if destinations is not UNSET:
            field_dict["destinations"] = destinations
        if headers is not UNSET:
            field_dict["headers"] = headers
        if secrets is not UNSET:
            field_dict["secrets"] = secrets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.proxy_target_body import ProxyTargetBody
        from ..models.proxy_target_headers import ProxyTargetHeaders
        from ..models.proxy_target_secrets import ProxyTargetSecrets

        if not src_dict:
            return None
        d = src_dict.copy()
        _body = d.pop("body", UNSET)
        body: Union[Unset, ProxyTargetBody]
        if isinstance(_body, Unset):
            body = UNSET
        else:
            body = ProxyTargetBody.from_dict(_body)

        destinations = cast(list[str], d.pop("destinations", UNSET))

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, ProxyTargetHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = ProxyTargetHeaders.from_dict(_headers)

        _secrets = d.pop("secrets", UNSET)
        secrets: Union[Unset, ProxyTargetSecrets]
        if isinstance(_secrets, Unset):
            secrets = UNSET
        else:
            secrets = ProxyTargetSecrets.from_dict(_secrets)

        proxy_target = cls(
            body=body,
            destinations=destinations,
            headers=headers,
            secrets=secrets,
        )

        proxy_target.additional_properties = d
        return proxy_target

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
