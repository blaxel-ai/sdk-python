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
    """Volume resource for persistent storage

    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, VolumeSpec]): Volume specification - immutable configuration
        state (Union[Unset, VolumeState]): Volume state - mutable runtime state
        status (Union[Unset, str]): Volume status computed from events
        terminated_at (Union[Unset, str]): Timestamp when the volume was marked for termination
    """

    events: Union[Unset, list["CoreEvent"]] = UNSET
    metadata: Union[Unset, "Metadata"] = UNSET
    spec: Union[Unset, "VolumeSpec"] = UNSET
    state: Union[Unset, "VolumeState"] = UNSET
    status: Union[Unset, str] = UNSET
    terminated_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for componentsschemas_core_events_item_data in self.events:
                if type(componentsschemas_core_events_item_data) is dict:
                    componentsschemas_core_events_item = componentsschemas_core_events_item_data
                else:
                    componentsschemas_core_events_item = componentsschemas_core_events_item_data.to_dict()
                events.append(componentsschemas_core_events_item)

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if self.metadata and not isinstance(self.metadata, Unset) and not isinstance(self.metadata, dict):
            metadata = self.metadata.to_dict()
        elif self.metadata and isinstance(self.metadata, dict):
            metadata = self.metadata

        spec: Union[Unset, dict[str, Any]] = UNSET
        if self.spec and not isinstance(self.spec, Unset) and not isinstance(self.spec, dict):
            spec = self.spec.to_dict()
        elif self.spec and isinstance(self.spec, dict):
            spec = self.spec

        state: Union[Unset, dict[str, Any]] = UNSET
        if self.state and not isinstance(self.state, Unset) and not isinstance(self.state, dict):
            state = self.state.to_dict()
        elif self.state and isinstance(self.state, dict):
            state = self.state

        status = self.status

        terminated_at = self.terminated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if events is not UNSET:
            field_dict["events"] = events
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if spec is not UNSET:
            field_dict["spec"] = spec
        if state is not UNSET:
            field_dict["state"] = state
        if status is not UNSET:
            field_dict["status"] = status
        if terminated_at is not UNSET:
            field_dict["terminatedAt"] = terminated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.core_event import CoreEvent
        from ..models.metadata import Metadata
        from ..models.volume_spec import VolumeSpec
        from ..models.volume_state import VolumeState

        if not src_dict:
            return None
        d = src_dict.copy()
        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(componentsschemas_core_events_item_data)

            events.append(componentsschemas_core_events_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        _spec = d.pop("spec", UNSET)
        spec: Union[Unset, VolumeSpec]
        if isinstance(_spec, Unset):
            spec = UNSET
        else:
            spec = VolumeSpec.from_dict(_spec)

        _state = d.pop("state", UNSET)
        state: Union[Unset, VolumeState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = VolumeState.from_dict(_state)

        status = d.pop("status", UNSET)

        terminated_at = d.pop("terminatedAt", UNSET)

        volume = cls(
            events=events,
            metadata=metadata,
            spec=spec,
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
