from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.core_event import CoreEvent
    from ..models.metadata import Metadata
    from ..models.sandbox_spec import SandboxSpec


T = TypeVar("T", bound="Sandbox")


@_attrs_define
class Sandbox:
    """Lightweight virtual machine for secure AI code execution. Sandboxes resume from standby in under 25ms and
    automatically scale to zero after inactivity, preserving memory state including running processes and filesystem.

        Attributes:
            metadata (Metadata): Common metadata fields shared by all Blaxel resources including name, labels, timestamps,
                and ownership information
            spec (SandboxSpec): Configuration for a sandbox including its image, memory, ports, region, and lifecycle
                policies
            events (Union[Unset, list['CoreEvent']]): Events happening on a resource deployed on Blaxel
            last_used_at (Union[Unset, str]): Last time the sandbox was used (read-only, managed by the system)
            status (Union[Unset, Status]): Deployment status of a resource deployed on Blaxel
    """

    metadata: "Metadata"
    spec: "SandboxSpec"
    events: Union[Unset, list["CoreEvent"]] = UNSET
    last_used_at: Union[Unset, str] = UNSET
    status: Union[Unset, Status] = UNSET
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

        last_used_at = self.last_used_at

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

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
        if last_used_at is not UNSET:
            field_dict["lastUsedAt"] = last_used_at
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.core_event import CoreEvent
        from ..models.metadata import Metadata
        from ..models.sandbox_spec import SandboxSpec

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = Metadata.from_dict(d.pop("metadata"))

        spec = SandboxSpec.from_dict(d.pop("spec"))

        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(
                componentsschemas_core_events_item_data
            )

            events.append(componentsschemas_core_events_item)

        last_used_at = d.pop("lastUsedAt", d.pop("last_used_at", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = Status(_status)

        sandbox = cls(
            metadata=metadata,
            spec=spec,
            events=events,
            last_used_at=last_used_at,
            status=status,
        )

        sandbox.additional_properties = d
        return sandbox

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
