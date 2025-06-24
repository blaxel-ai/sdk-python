from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationRepository")


@_attrs_define
class IntegrationRepository:
    """Integration repository

    Attributes:
        id (Union[Unset, str]): Repository ID
        is_bl (Union[Unset, bool]): Whether the repository has Blaxel imports
        name (Union[Unset, str]): Repository name
        organization (Union[Unset, str]): Repository owner
        url (Union[Unset, str]): Repository URL
    """

    id: Union[Unset, str] = UNSET
    is_bl: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        is_bl = self.is_bl

        name = self.name

        organization = self.organization

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if is_bl is not UNSET:
            field_dict["isBl"] = is_bl
        if name is not UNSET:
            field_dict["name"] = name
        if organization is not UNSET:
            field_dict["organization"] = organization
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        is_bl = d.pop("isBl", UNSET)

        name = d.pop("name", UNSET)

        organization = d.pop("organization", UNSET)

        url = d.pop("url", UNSET)

        integration_repository = cls(
            id=id,
            is_bl=is_bl,
            name=name,
            organization=organization,
            url=url,
        )

        integration_repository.additional_properties = d
        return integration_repository

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
