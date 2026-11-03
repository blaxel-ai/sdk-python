from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pending_invitation_render_account import PendingInvitationRenderAccount
    from ..models.pending_invitation_render_invited_by import PendingInvitationRenderInvitedBy
    from ..models.pending_invitation_render_workspace import PendingInvitationRenderWorkspace
    from ..models.pending_invitation_workspace_details import PendingInvitationWorkspaceDetails


T = TypeVar("T", bound="PendingInvitationRender")


@_attrs_define
class PendingInvitationRender:
    """Pending invitation in workspace

    Attributes:
        account (PendingInvitationRenderAccount | Unset): Account info in pending invitation render (for account_admin
            type)
        email (str | Unset): User email
        expires_at (str | Unset): The date and time when the invitation expires
        invitation_id (str | Unset): Opaque invitation identifier
        invited_at (str | Unset): Invitation date
        invited_by (PendingInvitationRenderInvitedBy | Unset): Invited by
        role (str | Unset): ACL role
        type_ (str | Unset): Invitation type: "workspace" or "account_admin"
        workspace (PendingInvitationRenderWorkspace | Unset): Workspace
        workspace_details (PendingInvitationWorkspaceDetails | Unset): Workspace details
    """

    account: PendingInvitationRenderAccount | Unset = UNSET
    email: str | Unset = UNSET
    expires_at: str | Unset = UNSET
    invitation_id: str | Unset = UNSET
    invited_at: str | Unset = UNSET
    invited_by: PendingInvitationRenderInvitedBy | Unset = UNSET
    role: str | Unset = UNSET
    type_: str | Unset = UNSET
    workspace: PendingInvitationRenderWorkspace | Unset = UNSET
    workspace_details: PendingInvitationWorkspaceDetails | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account: dict[str, Any] | Unset = UNSET
        if (
            self.account
            and not isinstance(self.account, Unset)
            and not isinstance(self.account, dict)
        ):
            account = self.account.to_dict()
        elif self.account and isinstance(self.account, dict):
            account = self.account

        email = self.email

        expires_at = self.expires_at

        invitation_id = self.invitation_id

        invited_at = self.invited_at

        invited_by: dict[str, Any] | Unset = UNSET
        if (
            self.invited_by
            and not isinstance(self.invited_by, Unset)
            and not isinstance(self.invited_by, dict)
        ):
            invited_by = self.invited_by.to_dict()
        elif self.invited_by and isinstance(self.invited_by, dict):
            invited_by = self.invited_by

        role = self.role

        type_ = self.type_

        workspace: dict[str, Any] | Unset = UNSET
        if (
            self.workspace
            and not isinstance(self.workspace, Unset)
            and not isinstance(self.workspace, dict)
        ):
            workspace = self.workspace.to_dict()
        elif self.workspace and isinstance(self.workspace, dict):
            workspace = self.workspace

        workspace_details: dict[str, Any] | Unset = UNSET
        if (
            self.workspace_details
            and not isinstance(self.workspace_details, Unset)
            and not isinstance(self.workspace_details, dict)
        ):
            workspace_details = self.workspace_details.to_dict()
        elif self.workspace_details and isinstance(self.workspace_details, dict):
            workspace_details = self.workspace_details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if email is not UNSET:
            field_dict["email"] = email
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if invitation_id is not UNSET:
            field_dict["invitationId"] = invitation_id
        if invited_at is not UNSET:
            field_dict["invitedAt"] = invited_at
        if invited_by is not UNSET:
            field_dict["invitedBy"] = invited_by
        if role is not UNSET:
            field_dict["role"] = role
        if type_ is not UNSET:
            field_dict["type"] = type_
        if workspace is not UNSET:
            field_dict["workspace"] = workspace
        if workspace_details is not UNSET:
            field_dict["workspaceDetails"] = workspace_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.pending_invitation_render_account import (
            PendingInvitationRenderAccount,  # noqa: PLC0415
        )
        from ..models.pending_invitation_render_invited_by import (
            PendingInvitationRenderInvitedBy,  # noqa: PLC0415
        )
        from ..models.pending_invitation_render_workspace import (
            PendingInvitationRenderWorkspace,  # noqa: PLC0415
        )
        from ..models.pending_invitation_workspace_details import (
            PendingInvitationWorkspaceDetails,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        _account = d.pop("account", UNSET)
        account: PendingInvitationRenderAccount | Unset
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = PendingInvitationRenderAccount.from_dict(_account)

        email = d.pop("email", UNSET)

        expires_at = d.pop("expiresAt", d.pop("expires_at", UNSET))

        invitation_id = d.pop("invitationId", d.pop("invitation_id", UNSET))

        invited_at = d.pop("invitedAt", d.pop("invited_at", UNSET))

        _invited_by = d.pop("invitedBy", d.pop("invited_by", UNSET))
        invited_by: PendingInvitationRenderInvitedBy | Unset
        if isinstance(_invited_by, Unset):
            invited_by = UNSET
        else:
            invited_by = PendingInvitationRenderInvitedBy.from_dict(_invited_by)

        role = d.pop("role", UNSET)

        type_ = d.pop("type", d.pop("type_", UNSET))

        _workspace = d.pop("workspace", UNSET)
        workspace: PendingInvitationRenderWorkspace | Unset
        if isinstance(_workspace, Unset):
            workspace = UNSET
        else:
            workspace = PendingInvitationRenderWorkspace.from_dict(_workspace)

        _workspace_details = d.pop("workspaceDetails", d.pop("workspace_details", UNSET))
        workspace_details: PendingInvitationWorkspaceDetails | Unset
        if isinstance(_workspace_details, Unset):
            workspace_details = UNSET
        else:
            workspace_details = PendingInvitationWorkspaceDetails.from_dict(_workspace_details)

        pending_invitation_render = cls(
            account=account,
            email=email,
            expires_at=expires_at,
            invitation_id=invitation_id,
            invited_at=invited_at,
            invited_by=invited_by,
            role=role,
            type_=type_,
            workspace=workspace,
            workspace_details=workspace_details,
        )

        pending_invitation_render.additional_properties = d
        return pending_invitation_render

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
