from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SSODomainMetadata")


@_attrs_define
class SSODomainMetadata:
    """SSO domain metadata

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        account_id (Union[Unset, str]): Account ID
        display_name (Union[Unset, str]): Display name for the SSO domain Example: Acme Corp.
        name (Union[Unset, str]): Domain name (e.g., "acme.com") Example: acme.com.
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        account_id = self.account_id

        display_name = self.display_name

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        updated_by = d.pop("updatedBy", d.pop("updated_by", UNSET))

        account_id = d.pop("accountId", d.pop("account_id", UNSET))

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        name = d.pop("name", UNSET)

        sso_domain_metadata = cls(
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            account_id=account_id,
            display_name=display_name,
            name=name,
        )

        sso_domain_metadata.additional_properties = d
        return sso_domain_metadata

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
