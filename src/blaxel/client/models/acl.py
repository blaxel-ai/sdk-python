from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ACL")


@_attrs_define
class ACL:
    """ACL

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        id (Union[Unset, str]): ACL id
        resource_id (Union[Unset, str]): Resource ID
        resource_type (Union[Unset, str]): Resource type
        role (Union[Unset, str]): Role
        subject_id (Union[Unset, str]): Subject ID
        subject_type (Union[Unset, str]): Subject type
        workspace (Union[Unset, str]): Workspace name
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    resource_id: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    subject_id: Union[Unset, str] = UNSET
    subject_type: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        id = self.id

        resource_id = self.resource_id

        resource_type = self.resource_type

        role = self.role

        subject_id = self.subject_id

        subject_type = self.subject_type

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if id is not UNSET:
            field_dict["id"] = id
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if role is not UNSET:
            field_dict["role"] = role
        if subject_id is not UNSET:
            field_dict["subject_id"] = subject_id
        if subject_type is not UNSET:
            field_dict["subject_type"] = subject_type
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        id = d.pop("id", UNSET)

        resource_id = d.pop("resource_id", UNSET)

        resource_type = d.pop("resource_type", UNSET)

        role = d.pop("role", UNSET)

        subject_id = d.pop("subject_id", UNSET)

        subject_type = d.pop("subject_type", UNSET)

        workspace = d.pop("workspace", UNSET)

        acl = cls(
            created_at=created_at,
            updated_at=updated_at,
            id=id,
            resource_id=resource_id,
            resource_type=resource_type,
            role=role,
            subject_id=subject_id,
            subject_type=subject_type,
            workspace=workspace,
        )

        acl.additional_properties = d
        return acl

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
