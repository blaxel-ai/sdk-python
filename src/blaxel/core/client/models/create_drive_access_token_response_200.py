from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDriveAccessTokenResponse200")


@_attrs_define
class CreateDriveAccessTokenResponse200:
    """
    Attributes:
        access_token (Union[Unset, str]):
        expires_in (Union[Unset, float]):
        token_type (Union[Unset, str]):  Example: Bearer.
    """

    access_token: Union[Unset, str] = UNSET
    expires_in: Union[Unset, float] = UNSET
    token_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        expires_in = self.expires_in

        token_type = self.token_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if access_token is not UNSET:
            field_dict["access_token"] = access_token
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if token_type is not UNSET:
            field_dict["token_type"] = token_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        access_token = d.pop("access_token", UNSET)

        expires_in = d.pop("expires_in", UNSET)

        token_type = d.pop("token_type", UNSET)

        create_drive_access_token_response_200 = cls(
            access_token=access_token,
            expires_in=expires_in,
            token_type=token_type,
        )

        create_drive_access_token_response_200.additional_properties = d
        return create_drive_access_token_response_200

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
