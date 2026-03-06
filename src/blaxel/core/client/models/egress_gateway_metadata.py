from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EgressGatewayMetadata")


@_attrs_define
class EgressGatewayMetadata:
    """Metadata for an egress gateway resource including workspace, VPC, and name

    Attributes:
        name (str): Unique identifier for the egress gateway within the VPC. Must be lowercase alphanumeric with
            hyphens, max 49 characters. Immutable after creation. Example: my-egress-gateway.
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        display_name (Union[Unset, str]): Human-readable name for display in the UI. Can contain spaces and special
            characters, max 63 characters. Example: My Egress Gateway.
        vpc_name (Union[Unset, str]): Name of the VPC this egress gateway belongs to
        workspace (Union[Unset, str]): Name of the workspace this resource belongs to (read-only, set automatically)
    """

    name: str
    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    vpc_name: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        display_name = self.display_name

        vpc_name = self.vpc_name

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if vpc_name is not UNSET:
            field_dict["vpcName"] = vpc_name
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name")

        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        updated_by = d.pop("updatedBy", d.pop("updated_by", UNSET))

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        vpc_name = d.pop("vpcName", d.pop("vpc_name", UNSET))

        workspace = d.pop("workspace", UNSET)

        egress_gateway_metadata = cls(
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            display_name=display_name,
            vpc_name=vpc_name,
            workspace=workspace,
        )

        egress_gateway_metadata.additional_properties = d
        return egress_gateway_metadata

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
