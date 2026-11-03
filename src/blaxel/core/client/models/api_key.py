from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiKey")


@_attrs_define
class ApiKey:
    """Long-lived API key for accessing Blaxel

    Attributes:
        created_at (str | Unset): The date and time when the resource was created
        updated_at (str | Unset): The date and time when the resource was updated
        created_by (str | Unset): The user or service account who created the resource
        updated_by (str | Unset): The user or service account who updated the resource
        api_key (str | Unset): Api key
        expires_in (str | Unset): Duration until expiration. Supports formats like '30d' (30 days), '24h' (24 hours),
            '1w' (1 week). Must be positive and at most 10 years. If not set, the API key never expires. Example: 30d.
        id (str | Unset): Api key id, to retrieve it from the API Example: ak_abc123def456.
        name (str | Unset): Name for the API key Example: CI/CD Pipeline Key.
        sub (str | Unset): User subject identifier
        sub_type (str | Unset): Subject type (user or service_account) Example: user.
    """

    created_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    created_by: str | Unset = UNSET
    updated_by: str | Unset = UNSET
    api_key: str | Unset = UNSET
    expires_in: str | Unset = UNSET
    id: str | Unset = UNSET
    name: str | Unset = UNSET
    sub: str | Unset = UNSET
    sub_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        api_key = self.api_key

        expires_in = self.expires_in

        id = self.id

        name = self.name

        sub = self.sub

        sub_type = self.sub_type

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
        if api_key is not UNSET:
            field_dict["apiKey"] = api_key
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if sub is not UNSET:
            field_dict["sub"] = sub
        if sub_type is not UNSET:
            field_dict["sub_type"] = sub_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        updated_by = d.pop("updatedBy", d.pop("updated_by", UNSET))

        api_key = d.pop("apiKey", d.pop("api_key", UNSET))

        expires_in = d.pop("expires_in", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        sub = d.pop("sub", UNSET)

        sub_type = d.pop("sub_type", UNSET)

        api_key = cls(
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            api_key=api_key,
            expires_in=expires_in,
            id=id,
            name=name,
            sub=sub,
            sub_type=sub_type,
        )

        api_key.additional_properties = d
        return api_key

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
