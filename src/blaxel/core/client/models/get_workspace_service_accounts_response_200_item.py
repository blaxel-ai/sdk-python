from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWorkspaceServiceAccountsResponse200Item")


@_attrs_define
class GetWorkspaceServiceAccountsResponse200Item:
    """
    Attributes:
        client_id (str | Unset): Service account client ID
        created_at (str | Unset): Creation timestamp
        description (str | Unset): Service account description
        name (str | Unset): Service account name
        role (str | Unset): Role of the service account in the workspace
        updated_at (str | Unset): Last update timestamp
    """

    client_id: str | Unset = UNSET
    created_at: str | Unset = UNSET
    description: str | Unset = UNSET
    name: str | Unset = UNSET
    role: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        created_at = self.created_at

        description = self.description

        name = self.name

        role = self.role

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if role is not UNSET:
            field_dict["role"] = role
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        client_id = d.pop("client_id", UNSET)

        created_at = d.pop("created_at", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        role = d.pop("role", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        get_workspace_service_accounts_response_200_item = cls(
            client_id=client_id,
            created_at=created_at,
            description=description,
            name=name,
            role=role,
            updated_at=updated_at,
        )

        get_workspace_service_accounts_response_200_item.additional_properties = d
        return get_workspace_service_accounts_response_200_item

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
