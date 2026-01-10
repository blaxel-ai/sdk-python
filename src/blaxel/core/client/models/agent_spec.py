from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_runtime import AgentRuntime
    from ..models.repository import Repository
    from ..models.revision_configuration import RevisionConfiguration
    from ..models.trigger import Trigger


T = TypeVar("T", bound="AgentSpec")


@_attrs_define
class AgentSpec:
    """Configuration for an AI agent including runtime settings, repository source, and deployment triggers

    Attributes:
        enabled (Union[Unset, bool]): When false, the agent is disabled and will not serve inference requests Default:
            True. Example: True.
        policies (Union[Unset, list[str]]):
        repository (Union[Unset, Repository]): Repository
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, AgentRuntime]): Runtime configuration defining how the AI agent is deployed and scaled
            globally
        triggers (Union[Unset, list['Trigger']]): Triggers to use your agent
    """

    enabled: Union[Unset, bool] = True
    policies: Union[Unset, list[str]] = UNSET
    repository: Union[Unset, "Repository"] = UNSET
    revision: Union[Unset, "RevisionConfiguration"] = UNSET
    runtime: Union[Unset, "AgentRuntime"] = UNSET
    triggers: Union[Unset, list["Trigger"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        policies: Union[Unset, list[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        repository: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.repository
            and not isinstance(self.repository, Unset)
            and not isinstance(self.repository, dict)
        ):
            repository = self.repository.to_dict()
        elif self.repository and isinstance(self.repository, dict):
            repository = self.repository

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
        if policies is not UNSET:
            field_dict["policies"] = policies
        if repository is not UNSET:
            field_dict["repository"] = repository
        if revision is not UNSET:
            field_dict["revision"] = revision
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.agent_runtime import AgentRuntime
        from ..models.repository import Repository
        from ..models.revision_configuration import RevisionConfiguration
        from ..models.trigger import Trigger

        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        policies = cast(list[str], d.pop("policies", UNSET))

        _repository = d.pop("repository", UNSET)
        repository: Union[Unset, Repository]
        if isinstance(_repository, Unset):
            repository = UNSET
        else:
            repository = Repository.from_dict(_repository)

        _revision = d.pop("revision", UNSET)
        revision: Union[Unset, RevisionConfiguration]
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = RevisionConfiguration.from_dict(_revision)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, AgentRuntime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = AgentRuntime.from_dict(_runtime)

        triggers = []
        _triggers = d.pop("triggers", UNSET)
        for componentsschemas_triggers_item_data in _triggers or []:
            componentsschemas_triggers_item = Trigger.from_dict(
                componentsschemas_triggers_item_data
            )

            triggers.append(componentsschemas_triggers_item)

        agent_spec = cls(
            enabled=enabled,
            policies=policies,
            repository=repository,
            revision=revision,
            runtime=runtime,
            triggers=triggers,
        )

        agent_spec.additional_properties = d
        return agent_spec

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
