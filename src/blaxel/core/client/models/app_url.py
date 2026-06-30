from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppUrl")


@_attrs_define
class AppUrl:
    """A single URL entry for the application. If the domain is a wildcard custom domain (e.g. *.sandbox.vybe.build), use
    subdomain to pick a specific subdomain. If the domain is a direct custom domain (e.g. app.vybe.build), subdomain is
    not needed.

        Attributes:
            domain (str): Custom domain (must be a verified custom domain in the workspace). Can be a wildcard domain (e.g.
                sandbox.vybe.build registered as *.sandbox.vybe.build) or a direct domain (e.g. app.vybe.build). Example:
                app.example.com.
            subdomain (Union[Unset, str]): Subdomain to use with a wildcard custom domain (optional) Example: www.
    """

    domain: str
    subdomain: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        domain = self.domain

        subdomain = self.subdomain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
            }
        )
        if subdomain is not UNSET:
            field_dict["subdomain"] = subdomain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        domain = d.pop("domain")

        subdomain = d.pop("subdomain", UNSET)

        app_url = cls(
            domain=domain,
            subdomain=subdomain,
        )

        app_url.additional_properties = d
        return app_url

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
