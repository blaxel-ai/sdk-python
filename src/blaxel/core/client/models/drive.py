from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.core_event import CoreEvent
    from ..models.drive_spec import DriveSpec
    from ..models.drive_state import DriveState
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Drive")


@_attrs_define
class Drive:
    """Drive providing persistent storage that can be attached to agents, functions, and sandboxes. Drives are backed by
    SeaweedFS buckets and can be mounted at runtime via the sbx API.

        Attributes:
            metadata (Metadata): Common metadata fields shared by all Blaxel resources including name, labels, timestamps,
                and ownership information
            spec (DriveSpec): Immutable drive configuration set at creation time
            events (Union[Unset, list['CoreEvent']]): Events happening on a resource deployed on Blaxel
            state (Union[Unset, DriveState]): Current runtime state of the drive
            status (Union[Unset, str]): Drive status computed from events
    """

    metadata: "Metadata"
    spec: "DriveSpec"
    events: Union[Unset, list["CoreEvent"]] = UNSET
    state: Union[Unset, "DriveState"] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if type(self.metadata) is dict:
            metadata = self.metadata
        else:
            metadata = self.metadata.to_dict()

        if type(self.spec) is dict:
            spec = self.spec
        else:
            spec = self.spec.to_dict()

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

        state: Union[Unset, dict[str, Any]] = UNSET
        if self.state and not isinstance(self.state, Unset) and not isinstance(self.state, dict):
            state = self.state.to_dict()
        elif self.state and isinstance(self.state, dict):
            state = self.state

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "spec": spec,
            }
        )
        if events is not UNSET:
            field_dict["events"] = events
        if state is not UNSET:
            field_dict["state"] = state
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.core_event import CoreEvent
        from ..models.drive_spec import DriveSpec
        from ..models.drive_state import DriveState
        from ..models.metadata import Metadata

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = Metadata.from_dict(d.pop("metadata"))

        spec = DriveSpec.from_dict(d.pop("spec"))

        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(
                componentsschemas_core_events_item_data
            )

            events.append(componentsschemas_core_events_item)

        _state = d.pop("state", UNSET)
        state: Union[Unset, DriveState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = DriveState.from_dict(_state)

        status = d.pop("status", UNSET)

        drive = cls(
            metadata=metadata,
            spec=spec,
            events=events,
            state=state,
            status=status,
        )

        drive.additional_properties = d
        return drive

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
