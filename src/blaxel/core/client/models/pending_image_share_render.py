from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PendingImageShareRender")


@_attrs_define
class PendingImageShareRender:
    """Rendered pending image share with source/target workspace metadata

    Attributes:
        created_at (Union[Unset, str]): Creation date
        expires_at (Union[Unset, str]): Expiration date
        has_conflict (Union[Unset, bool]): Whether the target workspace already has an image with the same name
            (potential conflict)
        id (Union[Unset, str]): Unique identifier for the pending image share
        image_name (Union[Unset, str]): Image name (repository)
        resource_type (Union[Unset, str]): Resource type (agent, function, sandbox, job)
        shared_by (Union[Unset, str]): User sub who initiated the share
        shared_by_email (Union[Unset, str]): Email of the user who initiated the share
        source_account_id (Union[Unset, str]): Source account ID
        source_workspace (Union[Unset, str]): Source workspace name
        source_workspace_display_name (Union[Unset, str]): Source workspace display name
        target_account_id (Union[Unset, str]): Target account ID
        target_workspace (Union[Unset, str]): Target workspace name
        target_workspace_display_name (Union[Unset, str]): Target workspace display name
    """

    created_at: Union[Unset, str] = UNSET
    expires_at: Union[Unset, str] = UNSET
    has_conflict: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    image_name: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    shared_by: Union[Unset, str] = UNSET
    shared_by_email: Union[Unset, str] = UNSET
    source_account_id: Union[Unset, str] = UNSET
    source_workspace: Union[Unset, str] = UNSET
    source_workspace_display_name: Union[Unset, str] = UNSET
    target_account_id: Union[Unset, str] = UNSET
    target_workspace: Union[Unset, str] = UNSET
    target_workspace_display_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        expires_at = self.expires_at

        has_conflict = self.has_conflict

        id = self.id

        image_name = self.image_name

        resource_type = self.resource_type

        shared_by = self.shared_by

        shared_by_email = self.shared_by_email

        source_account_id = self.source_account_id

        source_workspace = self.source_workspace

        source_workspace_display_name = self.source_workspace_display_name

        target_account_id = self.target_account_id

        target_workspace = self.target_workspace

        target_workspace_display_name = self.target_workspace_display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if has_conflict is not UNSET:
            field_dict["hasConflict"] = has_conflict
        if id is not UNSET:
            field_dict["id"] = id
        if image_name is not UNSET:
            field_dict["imageName"] = image_name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if shared_by is not UNSET:
            field_dict["sharedBy"] = shared_by
        if shared_by_email is not UNSET:
            field_dict["sharedByEmail"] = shared_by_email
        if source_account_id is not UNSET:
            field_dict["sourceAccountId"] = source_account_id
        if source_workspace is not UNSET:
            field_dict["sourceWorkspace"] = source_workspace
        if source_workspace_display_name is not UNSET:
            field_dict["sourceWorkspaceDisplayName"] = source_workspace_display_name
        if target_account_id is not UNSET:
            field_dict["targetAccountId"] = target_account_id
        if target_workspace is not UNSET:
            field_dict["targetWorkspace"] = target_workspace
        if target_workspace_display_name is not UNSET:
            field_dict["targetWorkspaceDisplayName"] = target_workspace_display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        expires_at = d.pop("expiresAt", d.pop("expires_at", UNSET))

        has_conflict = d.pop("hasConflict", d.pop("has_conflict", UNSET))

        id = d.pop("id", UNSET)

        image_name = d.pop("imageName", d.pop("image_name", UNSET))

        resource_type = d.pop("resourceType", d.pop("resource_type", UNSET))

        shared_by = d.pop("sharedBy", d.pop("shared_by", UNSET))

        shared_by_email = d.pop("sharedByEmail", d.pop("shared_by_email", UNSET))

        source_account_id = d.pop("sourceAccountId", d.pop("source_account_id", UNSET))

        source_workspace = d.pop("sourceWorkspace", d.pop("source_workspace", UNSET))

        source_workspace_display_name = d.pop(
            "sourceWorkspaceDisplayName", d.pop("source_workspace_display_name", UNSET)
        )

        target_account_id = d.pop("targetAccountId", d.pop("target_account_id", UNSET))

        target_workspace = d.pop("targetWorkspace", d.pop("target_workspace", UNSET))

        target_workspace_display_name = d.pop(
            "targetWorkspaceDisplayName", d.pop("target_workspace_display_name", UNSET)
        )

        pending_image_share_render = cls(
            created_at=created_at,
            expires_at=expires_at,
            has_conflict=has_conflict,
            id=id,
            image_name=image_name,
            resource_type=resource_type,
            shared_by=shared_by,
            shared_by_email=shared_by_email,
            source_account_id=source_account_id,
            source_workspace=source_workspace,
            source_workspace_display_name=source_workspace_display_name,
            target_account_id=target_account_id,
            target_workspace=target_workspace,
            target_workspace_display_name=target_workspace_display_name,
        )

        pending_image_share_render.additional_properties = d
        return pending_image_share_render

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
