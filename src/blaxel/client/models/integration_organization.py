from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationOrganization")


@_attrs_define
class IntegrationOrganization:
    """Integration organization

    Attributes:
        avatar_url (Union[Unset, str]): Provider organization avatar URL
        display_name (Union[Unset, str]): Provider organization display name
        id (Union[Unset, str]): Provider organization ID
        name (Union[Unset, str]): Provider organization name
    """

    avatar_url: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_url = self.avatar_url

        display_name = self.display_name

        id = self.id

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        avatar_url = d.pop("avatar_url", UNSET)

        display_name = d.pop("displayName", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        integration_organization = cls(
            avatar_url=avatar_url,
            display_name=display_name,
            id=id,
            name=name,
        )

        integration_organization.additional_properties = d
        return integration_organization

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
