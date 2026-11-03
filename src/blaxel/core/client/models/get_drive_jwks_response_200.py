from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_drive_jwks_response_200_keys_item import GetDriveJwksResponse200KeysItem


T = TypeVar("T", bound="GetDriveJwksResponse200")


@_attrs_define
class GetDriveJwksResponse200:
    """
    Attributes:
        keys (list[GetDriveJwksResponse200KeysItem] | Unset):
    """

    keys: list[GetDriveJwksResponse200KeysItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        keys: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                if type(keys_item_data) is dict:
                    keys_item = keys_item_data
                else:
                    keys_item = keys_item_data.to_dict()
                keys.append(keys_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keys is not UNSET:
            field_dict["keys"] = keys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.get_drive_jwks_response_200_keys_item import (
            GetDriveJwksResponse200KeysItem,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        keys = []
        _keys = d.pop("keys", UNSET)
        for keys_item_data in _keys or []:
            keys_item = GetDriveJwksResponse200KeysItem.from_dict(keys_item_data)

            keys.append(keys_item)

        get_drive_jwks_response_200 = cls(
            keys=keys,
        )

        get_drive_jwks_response_200.additional_properties = d
        return get_drive_jwks_response_200

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
