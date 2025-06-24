from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PendingInvitationRenderInvitedBy")


@_attrs_define
class PendingInvitationRenderInvitedBy:
    """Invited by

    Attributes:
        email (Union[Unset, str]): User email
        family_name (Union[Unset, str]): User family name
        given_name (Union[Unset, str]): User given name
        sub (Union[Unset, str]): User sub
    """

    email: Union[Unset, str] = UNSET
    family_name: Union[Unset, str] = UNSET
    given_name: Union[Unset, str] = UNSET
    sub: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        family_name = self.family_name

        given_name = self.given_name

        sub = self.sub

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if family_name is not UNSET:
            field_dict["family_name"] = family_name
        if given_name is not UNSET:
            field_dict["given_name"] = given_name
        if sub is not UNSET:
            field_dict["sub"] = sub

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        family_name = d.pop("family_name", UNSET)

        given_name = d.pop("given_name", UNSET)

        sub = d.pop("sub", UNSET)

        pending_invitation_render_invited_by = cls(
            email=email,
            family_name=family_name,
            given_name=given_name,
            sub=sub,
        )

        pending_invitation_render_invited_by.additional_properties = d
        return pending_invitation_render_invited_by

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
