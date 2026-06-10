from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomDomainSubdomain")


@_attrs_define
class CustomDomainSubdomain:
    """A subdomain (preview) using a custom domain

    Attributes:
        preview_name (Union[Unset, str]): Preview name
        resource_name (Union[Unset, str]): Resource name
        resource_type (Union[Unset, str]): Resource type (e.g., sandbox)
        subdomain (Union[Unset, str]): Subdomain prefix used for routing
        url (Union[Unset, str]): Full URL of the preview on this custom domain
    """

    preview_name: Union[Unset, str] = UNSET
    resource_name: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    subdomain: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        preview_name = self.preview_name

        resource_name = self.resource_name

        resource_type = self.resource_type

        subdomain = self.subdomain

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if preview_name is not UNSET:
            field_dict["previewName"] = preview_name
        if resource_name is not UNSET:
            field_dict["resourceName"] = resource_name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if subdomain is not UNSET:
            field_dict["subdomain"] = subdomain
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        preview_name = d.pop("previewName", d.pop("preview_name", UNSET))

        resource_name = d.pop("resourceName", d.pop("resource_name", UNSET))

        resource_type = d.pop("resourceType", d.pop("resource_type", UNSET))

        subdomain = d.pop("subdomain", UNSET)

        url = d.pop("url", UNSET)

        custom_domain_subdomain = cls(
            preview_name=preview_name,
            resource_name=resource_name,
            resource_type=resource_type,
            subdomain=subdomain,
            url=url,
        )

        custom_domain_subdomain.additional_properties = d
        return custom_domain_subdomain

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
