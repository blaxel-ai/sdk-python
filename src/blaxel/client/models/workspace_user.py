from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceUser")


@_attrs_define
class WorkspaceUser:
    """Workspace user

    Attributes:
        accepted (Union[Unset, bool]): Whether the user has accepted the workspace invitation
        email (Union[Unset, str]): Workspace user email
        email_verified (Union[Unset, bool]): Whether the user's email has been verified
        family_name (Union[Unset, str]): Workspace user family name
        given_name (Union[Unset, str]): Workspace user given name
        role (Union[Unset, str]): Workspace user role
        sub (Union[Unset, str]): Workspace user identifier
    """

    accepted: Union[Unset, bool] = UNSET
    email: Union[Unset, str] = UNSET
    email_verified: Union[Unset, bool] = UNSET
    family_name: Union[Unset, str] = UNSET
    given_name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    sub: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accepted = self.accepted

        email = self.email

        email_verified = self.email_verified

        family_name = self.family_name

        given_name = self.given_name

        role = self.role

        sub = self.sub

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accepted is not UNSET:
            field_dict["accepted"] = accepted
        if email is not UNSET:
            field_dict["email"] = email
        if email_verified is not UNSET:
            field_dict["email_verified"] = email_verified
        if family_name is not UNSET:
            field_dict["family_name"] = family_name
        if given_name is not UNSET:
            field_dict["given_name"] = given_name
        if role is not UNSET:
            field_dict["role"] = role
        if sub is not UNSET:
            field_dict["sub"] = sub

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        accepted = d.pop("accepted", UNSET)

        email = d.pop("email", UNSET)

        email_verified = d.pop("email_verified", UNSET)

        family_name = d.pop("family_name", UNSET)

        given_name = d.pop("given_name", UNSET)

        role = d.pop("role", UNSET)

        sub = d.pop("sub", UNSET)

        workspace_user = cls(
            accepted=accepted,
            email=email,
            email_verified=email_verified,
            family_name=family_name,
            given_name=given_name,
            role=role,
            sub=sub,
        )

        workspace_user.additional_properties = d
        return workspace_user

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
