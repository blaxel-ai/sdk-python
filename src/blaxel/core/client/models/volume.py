from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.core_event import CoreEvent
    from ..models.metadata import Metadata
    from ..models.volume_spec import VolumeSpec
    from ..models.volume_state import VolumeState


T = TypeVar("T", bound="Volume")


@_attrs_define
class Volume:
    """Persistent storage volume that can be attached to sandboxes for durable file storage across sessions. Volumes
    survive sandbox deletion and can be reattached to new sandboxes.

        Attributes:
            metadata (Metadata): Common metadata fields shared by all Blaxel resources including name, labels, timestamps,
                and ownership information
            spec (VolumeSpec): Immutable volume configuration set at creation time (size and region cannot be changed after
                creation)
            events (Union[Unset, list['CoreEvent']]): Events happening on a resource deployed on Blaxel
            state (Union[Unset, VolumeState]): Current runtime state of the volume including attachment status
            status (Union[Unset, str]): Volume status computed from events
            terminated_at (Union[Unset, str]): Timestamp when the volume was marked for termination
    """

    metadata: "Metadata"
    spec: "VolumeSpec"
    events: Union[Unset, list["CoreEvent"]] = UNSET
    state: Union[Unset, "VolumeState"] = UNSET
    status: Union[Unset, str] = UNSET
    terminated_at: Union[Unset, str] = UNSET
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

        terminated_at = self.terminated_at

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
        if terminated_at is not UNSET:
            field_dict["terminatedAt"] = terminated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.core_event import CoreEvent
        from ..models.metadata import Metadata
        from ..models.volume_spec import VolumeSpec
        from ..models.volume_state import VolumeState

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = Metadata.from_dict(d.pop("metadata"))

        spec = VolumeSpec.from_dict(d.pop("spec"))

        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(
                componentsschemas_core_events_item_data
            )

            events.append(componentsschemas_core_events_item)

        _state = d.pop("state", UNSET)
        state: Union[Unset, VolumeState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = VolumeState.from_dict(_state)

        status = d.pop("status", UNSET)

        terminated_at = d.pop("terminatedAt", d.pop("terminated_at", UNSET))

        volume = cls(
            metadata=metadata,
            spec=spec,
            events=events,
            state=state,
            status=status,
            terminated_at=terminated_at,
        )

        volume.additional_properties = d
        return volume

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
