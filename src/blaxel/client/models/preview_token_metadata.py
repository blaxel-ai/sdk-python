from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewTokenMetadata")


@_attrs_define
class PreviewTokenMetadata:
    """PreviewTokenMetadata

    Attributes:
        name (Union[Unset, str]): Token name
        preview_name (Union[Unset, str]): Preview name
        resource_name (Union[Unset, str]): Resource name
        resource_type (Union[Unset, str]): Resource type
        workspace (Union[Unset, str]): Workspace name
    """

    name: Union[Unset, str] = UNSET
    preview_name: Union[Unset, str] = UNSET
    resource_name: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        preview_name = self.preview_name

        resource_name = self.resource_name

        resource_type = self.resource_type

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if preview_name is not UNSET:
            field_dict["previewName"] = preview_name
        if resource_name is not UNSET:
            field_dict["resourceName"] = resource_name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        preview_name = d.pop("previewName", UNSET)

        resource_name = d.pop("resourceName", UNSET)

        resource_type = d.pop("resourceType", UNSET)

        workspace = d.pop("workspace", UNSET)

        preview_token_metadata = cls(
            name=name,
            preview_name=preview_name,
            resource_name=resource_name,
            resource_type=resource_type,
            workspace=workspace,
        )

        preview_token_metadata.additional_properties = d
        return preview_token_metadata

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
