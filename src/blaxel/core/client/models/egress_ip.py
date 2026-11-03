from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.core_event import CoreEvent
    from ..models.egress_ip_metadata import EgressIPMetadata
    from ..models.egress_ip_spec import EgressIPSpec


T = TypeVar("T", bound="EgressIP")


@_attrs_define
class EgressIP:
    """An individual IP address allocated from an egress gateway for dedicated outbound traffic

    Attributes:
        metadata (EgressIPMetadata): Metadata for an egress IP address including gateway association and name
        spec (EgressIPSpec): Specification for an egress IP including IP family and the provisioned address
        events (list[CoreEvent] | Unset): Events happening on a resource deployed on Blaxel
        status (Status | Unset): Deployment status of a resource deployed on Blaxel
    """

    metadata: EgressIPMetadata
    spec: EgressIPSpec
    events: list[CoreEvent] | Unset = UNSET
    status: Status | Unset = UNSET
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

        events: list[dict[str, Any]] | Unset = UNSET
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

        status: str | Unset = UNSET
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
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.core_event import CoreEvent  # noqa: PLC0415
        from ..models.egress_ip_metadata import EgressIPMetadata  # noqa: PLC0415
        from ..models.egress_ip_spec import EgressIPSpec  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        metadata = EgressIPMetadata.from_dict(d.pop("metadata"))

        spec = EgressIPSpec.from_dict(d.pop("spec"))

        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(
                componentsschemas_core_events_item_data
            )

            events.append(componentsschemas_core_events_item)

        _status = d.pop("status", UNSET)
        status: Status | Unset
        if isinstance(_status, Unset) or _status == "":
            status = UNSET
        else:
            status = Status(_status)

        egress_ip = cls(
            metadata=metadata,
            spec=spec,
            events=events,
            status=status,
        )

        egress_ip.additional_properties = d
        return egress_ip

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
