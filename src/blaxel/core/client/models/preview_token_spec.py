from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewTokenSpec")


@_attrs_define
class PreviewTokenSpec:
    """Spec for a Preview Token

    Attributes:
        expired (bool | Unset): Whether the token is expired
        expires_at (str | Unset): Expiration time of the token
        token (str | Unset): Token
    """

    expired: bool | Unset = UNSET
    expires_at: str | Unset = UNSET
    token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expired = self.expired

        expires_at = self.expires_at

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expired is not UNSET:
            field_dict["expired"] = expired
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        expired = d.pop("expired", UNSET)

        expires_at = d.pop("expiresAt", d.pop("expires_at", UNSET))

        token = d.pop("token", UNSET)

        preview_token_spec = cls(
            expired=expired,
            expires_at=expires_at,
            token=token,
        )

        preview_token_spec.additional_properties = d
        return preview_token_spec

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
