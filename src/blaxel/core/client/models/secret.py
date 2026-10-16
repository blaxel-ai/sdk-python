from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
            created_at (Union[Unset, str]): The date and time when the secret was first created
            updated_at (Union[Unset, str]): The date and time of the latest version
            value (Union[Unset, str]): Secret value. Write-only, never returned by the API
    """

    destinations: list[str]
    name: str
    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destinations = self.destinations

        name = self.name

        created_at = self.created_at

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
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        destinations = cast(list[str], d.pop("destinations"))

        name = d.pop("name")

        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        value = d.pop("value", UNSET)

        secret = cls(
            destinations=destinations,
            name=name,
            created_at=created_at,
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
