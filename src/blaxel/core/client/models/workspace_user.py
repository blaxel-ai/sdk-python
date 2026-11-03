from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_user_source import WorkspaceUserSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceUser")


@_attrs_define
class WorkspaceUser:
    """Workspace user

    Attributes:
        accepted (bool | Unset): Whether the user has accepted the workspace invitation
        email (str | Unset): Workspace user email
        email_verified (bool | Unset): Whether the user's email has been verified
        expired (bool | Unset): Whether the invitation has expired
        family_name (str | Unset): Workspace user family name
        given_name (str | Unset): Workspace user given name
        mfa_enabled (bool | Unset): Whether the user has at least one verified MFA factor. Omitted when the caller is
            not entitled to see it (only workspace admins and owners see other members' MFA status) and for pending
            invitations, which have no account yet.
        role (str | Unset): Workspace user role
        source (WorkspaceUserSource | Unset): Source of the user provisioning
        sub (str | Unset): Workspace user identifier
    """

    accepted: bool | Unset = UNSET
    email: str | Unset = UNSET
    email_verified: bool | Unset = UNSET
    expired: bool | Unset = UNSET
    family_name: str | Unset = UNSET
    given_name: str | Unset = UNSET
    mfa_enabled: bool | Unset = UNSET
    role: str | Unset = UNSET
    source: WorkspaceUserSource | Unset = UNSET
    sub: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accepted = self.accepted

        email = self.email

        email_verified = self.email_verified

        expired = self.expired

        family_name = self.family_name

        given_name = self.given_name

        mfa_enabled = self.mfa_enabled

        role = self.role

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

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
        if expired is not UNSET:
            field_dict["expired"] = expired
        if family_name is not UNSET:
            field_dict["family_name"] = family_name
        if given_name is not UNSET:
            field_dict["given_name"] = given_name
        if mfa_enabled is not UNSET:
            field_dict["mfa_enabled"] = mfa_enabled
        if role is not UNSET:
            field_dict["role"] = role
        if source is not UNSET:
            field_dict["source"] = source
        if sub is not UNSET:
            field_dict["sub"] = sub

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        accepted = d.pop("accepted", UNSET)

        email = d.pop("email", UNSET)

        email_verified = d.pop("email_verified", UNSET)

        expired = d.pop("expired", UNSET)

        family_name = d.pop("family_name", UNSET)

        given_name = d.pop("given_name", UNSET)

        mfa_enabled = d.pop("mfa_enabled", UNSET)

        role = d.pop("role", UNSET)

        _source = d.pop("source", UNSET)
        source: WorkspaceUserSource | Unset
        if isinstance(_source, Unset) or _source == "":
            source = UNSET
        else:
            source = WorkspaceUserSource(_source)

        sub = d.pop("sub", UNSET)

        workspace_user = cls(
            accepted=accepted,
            email=email,
            email_verified=email_verified,
            expired=expired,
            family_name=family_name,
            given_name=given_name,
            mfa_enabled=mfa_enabled,
            role=role,
            source=source,
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
