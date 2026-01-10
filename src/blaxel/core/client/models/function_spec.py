from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.function_spec_transport import FunctionSpecTransport
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_runtime import FunctionRuntime
    from ..models.revision_configuration import RevisionConfiguration
    from ..models.trigger import Trigger


T = TypeVar("T", bound="FunctionSpec")


@_attrs_define
class FunctionSpec:
    """Configuration for an MCP server function including runtime settings, transport protocol, and connected integrations

    Attributes:
        enabled (Union[Unset, bool]): When false, the function is disabled and will not serve requests Default: True.
            Example: True.
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, FunctionRuntime]): Runtime configuration defining how the MCP server function is deployed
            and scaled
        transport (Union[Unset, FunctionSpecTransport]): Transport compatibility for the MCP, can be "websocket" or
            "http-stream" Example: http-stream.
        triggers (Union[Unset, list['Trigger']]): Triggers to use your agent
    """

    enabled: Union[Unset, bool] = True
    integration_connections: Union[Unset, list[str]] = UNSET
    policies: Union[Unset, list[str]] = UNSET
    revision: Union[Unset, "RevisionConfiguration"] = UNSET
    runtime: Union[Unset, "FunctionRuntime"] = UNSET
    transport: Union[Unset, FunctionSpecTransport] = UNSET
    triggers: Union[Unset, list["Trigger"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        integration_connections: Union[Unset, list[str]] = UNSET
        if not isinstance(self.integration_connections, Unset):
            integration_connections = self.integration_connections

        policies: Union[Unset, list[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        revision: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.revision
            and not isinstance(self.revision, Unset)
            and not isinstance(self.revision, dict)
        ):
            revision = self.revision.to_dict()
        elif self.revision and isinstance(self.revision, dict):
            revision = self.revision

        runtime: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.runtime
            and not isinstance(self.runtime, Unset)
            and not isinstance(self.runtime, dict)
        ):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

        transport: Union[Unset, str] = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.value

        triggers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = []
            for componentsschemas_triggers_item_data in self.triggers:
                if type(componentsschemas_triggers_item_data) is dict:
                    componentsschemas_triggers_item = componentsschemas_triggers_item_data
                else:
                    componentsschemas_triggers_item = componentsschemas_triggers_item_data.to_dict()
                triggers.append(componentsschemas_triggers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if integration_connections is not UNSET:
            field_dict["integrationConnections"] = integration_connections
        if policies is not UNSET:
            field_dict["policies"] = policies
        if revision is not UNSET:
            field_dict["revision"] = revision
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if transport is not UNSET:
            field_dict["transport"] = transport
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.function_runtime import FunctionRuntime
        from ..models.revision_configuration import RevisionConfiguration
        from ..models.trigger import Trigger

        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        integration_connections = cast(
            list[str], d.pop("integrationConnections", d.pop("integration_connections", UNSET))
        )

        policies = cast(list[str], d.pop("policies", UNSET))

        _revision = d.pop("revision", UNSET)
        revision: Union[Unset, RevisionConfiguration]
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = RevisionConfiguration.from_dict(_revision)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, FunctionRuntime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = FunctionRuntime.from_dict(_runtime)

        _transport = d.pop("transport", UNSET)
        transport: Union[Unset, FunctionSpecTransport]
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = FunctionSpecTransport(_transport)

        triggers = []
        _triggers = d.pop("triggers", UNSET)
        for componentsschemas_triggers_item_data in _triggers or []:
            componentsschemas_triggers_item = Trigger.from_dict(
                componentsschemas_triggers_item_data
            )

            triggers.append(componentsschemas_triggers_item)

        function_spec = cls(
            enabled=enabled,
            integration_connections=integration_connections,
            policies=policies,
            revision=revision,
            runtime=runtime,
            transport=transport,
            triggers=triggers,
        )

        function_spec.additional_properties = d
        return function_spec

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
