from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_spec import AgentSpec
    from ..models.core_event import CoreEvent
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Agent")


@_attrs_define
class Agent:
    """Serverless AI agent deployment that runs your custom agent code as an auto-scaling API endpoint. Agents are deployed
    from your code repository and expose a global inference URL for querying.

        Attributes:
            metadata (Metadata): Common metadata fields shared by all Blaxel resources including name, labels, timestamps,
                and ownership information
            spec (AgentSpec): Configuration for an AI agent including runtime settings, repository source, and deployment
                triggers
            events (Union[Unset, list['CoreEvent']]): Events happening on a resource deployed on Blaxel
            status (Union[Unset, Status]): Deployment status of a resource deployed on Blaxel
    """

    metadata: "Metadata"
    spec: "AgentSpec"
    events: Union[Unset, list["CoreEvent"]] = UNSET
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
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.agent_spec import AgentSpec
        from ..models.core_event import CoreEvent
        from ..models.metadata import Metadata

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = Metadata.from_dict(d.pop("metadata"))

        spec = AgentSpec.from_dict(d.pop("spec"))

        events = []
        _events = d.pop("events", UNSET)
        for componentsschemas_core_events_item_data in _events or []:
            componentsschemas_core_events_item = CoreEvent.from_dict(
                componentsschemas_core_events_item_data
            )

            events.append(componentsschemas_core_events_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = Status(_status)

        agent = cls(
            metadata=metadata,
            spec=spec,
            events=events,
            status=status,
        )

        agent.additional_properties = d
        return agent

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
