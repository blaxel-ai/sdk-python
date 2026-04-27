from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageShareTarget")


@_attrs_define
class ImageShareTarget:
    """
    Attributes:
        account_id (str): ID of the account that owns the target workspace.
        status (str): "active" when the share is applied in the target workspace, "pending" when it is awaiting accept
            on a cross-account share.
        workspace (str): The workspace the image is shared with.
        account_owner_email (Union[Unset, str]): Email of the account owner for the target workspace (when available).
        pending_share_id (Union[Unset, str]): ID of the pending share record when status is "pending".
        workspace_display_name (Union[Unset, str]): Display name of the target workspace.
    """

    account_id: str
    status: str
    workspace: str
    account_owner_email: Union[Unset, str] = UNSET
    pending_share_id: Union[Unset, str] = UNSET
    workspace_display_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = self.account_id

        status = self.status

        workspace = self.workspace

        account_owner_email = self.account_owner_email

        pending_share_id = self.pending_share_id

        workspace_display_name = self.workspace_display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "status": status,
                "workspace": workspace,
            }
        )
        if account_owner_email is not UNSET:
            field_dict["accountOwnerEmail"] = account_owner_email
        if pending_share_id is not UNSET:
            field_dict["pendingShareId"] = pending_share_id
        if workspace_display_name is not UNSET:
            field_dict["workspaceDisplayName"] = workspace_display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        account_id = d.pop("accountId") if "accountId" in d else d.pop("account_id")

        status = d.pop("status")

        workspace = d.pop("workspace")

        account_owner_email = d.pop("accountOwnerEmail", d.pop("account_owner_email", UNSET))

        pending_share_id = d.pop("pendingShareId", d.pop("pending_share_id", UNSET))

        workspace_display_name = d.pop(
            "workspaceDisplayName", d.pop("workspace_display_name", UNSET)
        )

        image_share_target = cls(
            account_id=account_id,
            status=status,
            workspace=workspace,
            account_owner_email=account_owner_email,
            pending_share_id=pending_share_id,
            workspace_display_name=workspace_display_name,
        )

        image_share_target.additional_properties = d
        return image_share_target

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
