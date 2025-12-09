from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageMetadata")


@_attrs_define
class ImageMetadata:
    """
    Attributes:
        created_at (Union[Unset, str]): The date and time when the image was created.
        display_name (Union[Unset, str]): The display name of the image (registry/workspace/repository).
        last_deployed_at (Union[Unset, str]): The date and time when the image was last deployed (most recent across all
            tags).
        name (Union[Unset, str]): The name of the image (repository name).
        resource_type (Union[Unset, str]): The resource type of the image.
        updated_at (Union[Unset, str]): The date and time when the image was last updated.
        workspace (Union[Unset, str]): The workspace of the image.
    """

    created_at: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    last_deployed_at: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        display_name = self.display_name

        last_deployed_at = self.last_deployed_at

        name = self.name

        resource_type = self.resource_type

        updated_at = self.updated_at

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if last_deployed_at is not UNSET:
            field_dict["lastDeployedAt"] = last_deployed_at
        if name is not UNSET:
            field_dict["name"] = name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        last_deployed_at = d.pop("lastDeployedAt", d.pop("last_deployed_at", UNSET))

        name = d.pop("name", UNSET)

        resource_type = d.pop("resourceType", d.pop("resource_type", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        workspace = d.pop("workspace", UNSET)

        image_metadata = cls(
            created_at=created_at,
            display_name=display_name,
            last_deployed_at=last_deployed_at,
            name=name,
            resource_type=resource_type,
            updated_at=updated_at,
            workspace=workspace,
        )

        image_metadata.additional_properties = d
        return image_metadata

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
