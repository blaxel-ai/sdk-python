from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkspaceServiceAccountResponse200")


@_attrs_define
class CreateWorkspaceServiceAccountResponse200:
    """
    Attributes:
        client_id (Union[Unset, str]): Service account client ID
        client_secret (Union[Unset, str]): Service account client secret (only returned on creation)
        created_at (Union[Unset, str]): Creation timestamp
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
        updated_at (Union[Unset, str]): Last update timestamp
    """

    client_id: Union[Unset, str] = UNSET
    client_secret: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        client_secret = self.client_secret

        created_at = self.created_at

        description = self.description

        name = self.name

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        created_at = d.pop("created_at", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        create_workspace_service_account_response_200 = cls(
            client_id=client_id,
            client_secret=client_secret,
            created_at=created_at,
            description=description,
            name=name,
            updated_at=updated_at,
        )

        create_workspace_service_account_response_200.additional_properties = d
        return create_workspace_service_account_response_200

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
