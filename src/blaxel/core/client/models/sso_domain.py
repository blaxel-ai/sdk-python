from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sso_domain_metadata import SSODomainMetadata
    from ..models.sso_domain_spec import SSODomainSpec


T = TypeVar("T", bound="SSODomain")


@_attrs_define
class SSODomain:
    """SSO domain for SAML-based Single Sign-On
    An SSO domain links an email domain (e.g., acme.com) to a workspace so that
    users with that email domain are redirected to the workspace's
    SSO/SAML identity provider during login.

        Attributes:
            metadata (SSODomainMetadata): SSO domain metadata
            spec (SSODomainSpec): SSO domain specification
    """

    metadata: "SSODomainMetadata"
    spec: "SSODomainSpec"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if type(self.metadata) is dict:
            metadata = self.metadata
        else:
            metadata = self.metadata.to_dict()

        if type(self.spec) is dict:
            spec = self.spec
        else:
            spec = self.spec.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "spec": spec,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sso_domain_metadata import SSODomainMetadata
        from ..models.sso_domain_spec import SSODomainSpec

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = SSODomainMetadata.from_dict(d.pop("metadata"))

        spec = SSODomainSpec.from_dict(d.pop("spec"))

        sso_domain = cls(
            metadata=metadata,
            spec=spec,
        )

        sso_domain.additional_properties = d
        return sso_domain

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
