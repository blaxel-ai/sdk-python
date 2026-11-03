from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PendingImageShare")


@_attrs_define
class PendingImageShare:
    """Pending cross-account image share awaiting approval from the destination workspace

    Attributes:
        created_at (str | Unset): The date and time when the resource was created
        updated_at (str | Unset): The date and time when the resource was updated
        created_by (str | Unset): The user or service account who created the resource
        updated_by (str | Unset): The user or service account who updated the resource
        expires_at (str | Unset): The date and time when the pending share expires
        id (str | Unset): Unique identifier for the pending image share
        image_name (str | Unset): Image name (repository)
        resource_type (str | Unset): Resource type (agent, function, sandbox, job)
        shared_by (str | Unset): User sub who initiated the share
        source_account_id (str | Unset): Source account ID
        source_workspace (str | Unset): Source workspace name
        target_account_id (str | Unset): Target account ID
        target_workspace (str | Unset): Target workspace name
    """

    created_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    created_by: str | Unset = UNSET
    updated_by: str | Unset = UNSET
    expires_at: str | Unset = UNSET
    id: str | Unset = UNSET
    image_name: str | Unset = UNSET
    resource_type: str | Unset = UNSET
    shared_by: str | Unset = UNSET
    source_account_id: str | Unset = UNSET
    source_workspace: str | Unset = UNSET
    target_account_id: str | Unset = UNSET
    target_workspace: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        expires_at = self.expires_at

        id = self.id

        image_name = self.image_name

        resource_type = self.resource_type

        shared_by = self.shared_by

        source_account_id = self.source_account_id

        source_workspace = self.source_workspace

        target_account_id = self.target_account_id

        target_workspace = self.target_workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if id is not UNSET:
            field_dict["id"] = id
        if image_name is not UNSET:
            field_dict["imageName"] = image_name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if shared_by is not UNSET:
            field_dict["sharedBy"] = shared_by
        if source_account_id is not UNSET:
            field_dict["sourceAccountId"] = source_account_id
        if source_workspace is not UNSET:
            field_dict["sourceWorkspace"] = source_workspace
        if target_account_id is not UNSET:
            field_dict["targetAccountId"] = target_account_id
        if target_workspace is not UNSET:
            field_dict["targetWorkspace"] = target_workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        updated_by = d.pop("updatedBy", d.pop("updated_by", UNSET))

        expires_at = d.pop("expiresAt", d.pop("expires_at", UNSET))

        id = d.pop("id", UNSET)

        image_name = d.pop("imageName", d.pop("image_name", UNSET))

        resource_type = d.pop("resourceType", d.pop("resource_type", UNSET))

        shared_by = d.pop("sharedBy", d.pop("shared_by", UNSET))

        source_account_id = d.pop("sourceAccountId", d.pop("source_account_id", UNSET))

        source_workspace = d.pop("sourceWorkspace", d.pop("source_workspace", UNSET))

        target_account_id = d.pop("targetAccountId", d.pop("target_account_id", UNSET))

        target_workspace = d.pop("targetWorkspace", d.pop("target_workspace", UNSET))

        pending_image_share = cls(
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            expires_at=expires_at,
            id=id,
            image_name=image_name,
            resource_type=resource_type,
            shared_by=shared_by,
            source_account_id=source_account_id,
            source_workspace=source_workspace,
            target_account_id=target_account_id,
            target_workspace=target_workspace,
        )

        pending_image_share.additional_properties = d
        return pending_image_share

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
