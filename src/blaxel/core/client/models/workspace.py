from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_labels import WorkspaceLabels
    from ..models.workspace_runtime import WorkspaceRuntime


T = TypeVar("T", bound="Workspace")


@_attrs_define
class Workspace:
    """Workspace

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        account_id (Union[Unset, str]): Workspace account id
        display_name (Union[Unset, str]): Workspace display name
        labels (Union[Unset, WorkspaceLabels]): Workspace labels
        name (Union[Unset, str]): Workspace name
        region (Union[Unset, str]): Workspace write region
        runtime (Union[Unset, WorkspaceRuntime]): Workspace runtime
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    labels: Union[Unset, "WorkspaceLabels"] = UNSET
    name: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    runtime: Union[Unset, "WorkspaceRuntime"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        account_id = self.account_id

        display_name = self.display_name

        labels: Union[Unset, dict[str, Any]] = UNSET
        if self.labels and not isinstance(self.labels, Unset) and not isinstance(self.labels, dict):
            labels = self.labels.to_dict()
        elif self.labels and isinstance(self.labels, dict):
            labels = self.labels

        name = self.name

        region = self.region

        runtime: Union[Unset, dict[str, Any]] = UNSET
        if self.runtime and not isinstance(self.runtime, Unset) and not isinstance(self.runtime, dict):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

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
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if labels is not UNSET:
            field_dict["labels"] = labels
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region
        if runtime is not UNSET:
            field_dict["runtime"] = runtime

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.workspace_labels import WorkspaceLabels
        from ..models.workspace_runtime import WorkspaceRuntime

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        updated_by = d.pop("updatedBy", UNSET)

        account_id = d.pop("accountId", UNSET)

        display_name = d.pop("displayName", UNSET)

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, WorkspaceLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = WorkspaceLabels.from_dict(_labels)

        name = d.pop("name", UNSET)

        region = d.pop("region", UNSET)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, WorkspaceRuntime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = WorkspaceRuntime.from_dict(_runtime)

        workspace = cls(
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            account_id=account_id,
            display_name=display_name,
            labels=labels,
            name=name,
            region=region,
            runtime=runtime,
        )

        workspace.additional_properties = d
        return workspace

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
