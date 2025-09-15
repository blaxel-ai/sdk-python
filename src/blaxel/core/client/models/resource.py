from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Resource")


@_attrs_define
class Resource:
    """Resource

    Attributes:
        infrastructure_generation (Union[Unset, str]): Region of the resource
        name (Union[Unset, str]): Name of the resource
        type_ (Union[Unset, str]): Type of the resource
        workspace (Union[Unset, str]): Workspace of the resource
        workspace_id (Union[Unset, str]): Workspace ID of the resource
    """

    infrastructure_generation: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        infrastructure_generation = self.infrastructure_generation

        name = self.name

        type_ = self.type_

        workspace = self.workspace

        workspace_id = self.workspace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if infrastructure_generation is not UNSET:
            field_dict["infrastructureGeneration"] = infrastructure_generation
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if workspace is not UNSET:
            field_dict["workspace"] = workspace
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        infrastructure_generation = d.pop("infrastructureGeneration", UNSET)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        workspace = d.pop("workspace", UNSET)

        workspace_id = d.pop("workspaceId", UNSET)

        resource = cls(
            infrastructure_generation=infrastructure_generation,
            name=name,
            type_=type_,
            workspace=workspace,
            workspace_id=workspace_id,
        )

        resource.additional_properties = d
        return resource

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
