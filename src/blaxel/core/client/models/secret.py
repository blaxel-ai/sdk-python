from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.secret_status import SecretStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Secret")


@_attrs_define
class Secret:
    """Workspace secret, referenced from proxy routing as {{SECRET:name}}. Values are write-only and can never be read
    back. Every upsert stores a new immutable version and the latest one is resolved at runtime, only for requests to
    its destinations.

        Attributes:
            destinations (list[str]): Destinations the secret resolves for, same syntax as routing destinations: a host,
                optionally followed by a path glob. The secret is never substituted toward any other destination. Example:
                ["api.stripe.com", "api.example.com/v1/*"].
            name (str): Case-sensitive secret name
            created_at (str | Unset): The date and time when the secret was first created
            status (SecretStatus | Unset): Delivery of the latest change to every region. Absent once every region applied
                it; PENDING while a region has not yet; DEGRADED when a region has been behind for more than 15 minutes;
                DELETING for a deleted secret not yet removed from every region.
            updated_at (str | Unset): The date and time of the latest version
            value (str | Unset): Secret value. Write-only, never returned by the API
    """

    destinations: list[str]
    name: str
    created_at: str | Unset = UNSET
    status: SecretStatus | Unset = UNSET
    updated_at: str | Unset = UNSET
    value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destinations = self.destinations

        name = self.name

        created_at = self.created_at

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        updated_at = self.updated_at

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destinations": destinations,
                "name": name,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if status is not UNSET:
            field_dict["status"] = status
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        destinations = cast(list[str], d.pop("destinations"))

        name = d.pop("name")

        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        _status = d.pop("status", UNSET)
        status: SecretStatus | Unset
        if isinstance(_status, Unset) or _status == "":
            status = UNSET
        else:
            status = SecretStatus(_status)

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        value = d.pop("value", UNSET)

        secret = cls(
            destinations=destinations,
            name=name,
            created_at=created_at,
            status=status,
            updated_at=updated_at,
            value=value,
        )

        secret.additional_properties = d
        return secret

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
