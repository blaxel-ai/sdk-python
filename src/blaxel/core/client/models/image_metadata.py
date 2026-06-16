from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.core_event import CoreEvent


T = TypeVar("T", bound="ImageMetadata")


@_attrs_define
class ImageMetadata:
    """
    Attributes:
        created_at (Union[Unset, str]): The date and time when the image was created.
        display_name (Union[Unset, str]): The display name of the image (registry/workspace/repository).
        events (Union[Unset, list['CoreEvent']]): Events happening on a resource deployed on Blaxel
        last_deployed_at (Union[Unset, str]): The date and time when the image was last deployed (most recent across all
            tags).
        name (Union[Unset, str]): The name of the image (repository name).
        resource_type (Union[Unset, str]): The resource type of the image.
        source_workspace (Union[Unset, str]): If this image is shared from another workspace, this field contains the
            name of the source workspace. Empty for non-shared images.
        status (Union[Unset, Status]): Deployment status of a resource deployed on Blaxel
        updated_at (Union[Unset, str]): The date and time when the image was last updated.
        workspace (Union[Unset, str]): The workspace of the image.
    """

    created_at: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    events: Union[Unset, list["CoreEvent"]] = UNSET
    last_deployed_at: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    source_workspace: Union[Unset, str] = UNSET
    status: Union[Unset, Status] = UNSET
    updated_at: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        created_at = self.created_at

        display_name = self.display_name

        events: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for componentsschemas_core_events_item_data in self.events:
                if type(componentsschemas_core_events_item_data) is dict:
                    componentsschemas_core_events_item = componentsschemas_core_events_item_data
                else:
                    componentsschemas_core_events_item = (
                        componentsschemas_core_events_item_data.to_dict()
                    )
                events.append(componentsschemas_core_events_item)

        last_deployed_at = self.last_deployed_at

        name = self.name

        resource_type = self.resource_type

        source_workspace = self.source_workspace

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        updated_at = self.updated_at

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if events is not UNSET:
            field_dict["events"] = events
        if last_deployed_at is not UNSET:
            field_dict["lastDeployedAt"] = last_deployed_at
        if name is not UNSET:
            field_dict["name"] = name
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if source_workspace is not UNSET:
            field_dict["sourceWorkspace"] = source_workspace
        if status is not UNSET:
            field_dict["status"] = status
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.core_event import CoreEvent

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(
                componentsschemas_core_events_item_data
            )

            events.append(componentsschemas_core_events_item)

        last_deployed_at = d.pop("lastDeployedAt", d.pop("last_deployed_at", UNSET))

        name = d.pop("name", UNSET)

        resource_type = d.pop("resourceType", d.pop("resource_type", UNSET))

        source_workspace = d.pop("sourceWorkspace", d.pop("source_workspace", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = Status(_status)

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        workspace = d.pop("workspace", UNSET)

        image_metadata = cls(
            created_at=created_at,
            display_name=display_name,
            events=events,
            last_deployed_at=last_deployed_at,
            name=name,
            resource_type=resource_type,
            source_workspace=source_workspace,
            status=status,
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
