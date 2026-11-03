from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_runtime import AgentRuntime
    from ..models.repository import Repository
    from ..models.revision_configuration import RevisionConfiguration
    from ..models.trigger import Trigger
    from ..models.volume_attachment import VolumeAttachment


T = TypeVar("T", bound="AgentSpec")


@_attrs_define
class AgentSpec:
    """Configuration for an AI agent including runtime settings, repository source, and deployment triggers

    Attributes:
        enabled (bool | Unset): When false, the agent is disabled and will not serve inference requests Default: True.
            Example: True.
        policies (list[str] | Unset):
        public (bool | Unset): When true, the agent is publicly accessible without authentication. Only available for
            mk3 generation. Default: False. Example: False.
        region (str | Unset): Region where the agent should be deployed (e.g. us-pdx-1, eu-lon-1). Required when volumes
            are attached. Example: us-pdx-1.
        repository (Repository | Unset): Repository
        revision (RevisionConfiguration | Unset): Revision configuration
        runtime (AgentRuntime | Unset): Runtime configuration defining how the AI agent is deployed and scaled globally
        triggers (list[Trigger] | Unset): Triggers to use your agent
        volumes (list[VolumeAttachment] | Unset):
    """

    enabled: bool | Unset = True
    policies: list[str] | Unset = UNSET
    public: bool | Unset = False
    region: str | Unset = UNSET
    repository: Repository | Unset = UNSET
    revision: RevisionConfiguration | Unset = UNSET
    runtime: AgentRuntime | Unset = UNSET
    triggers: list[Trigger] | Unset = UNSET
    volumes: list[VolumeAttachment] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        policies: list[str] | Unset = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        public = self.public

        region = self.region

        repository: dict[str, Any] | Unset = UNSET
        if (
            self.repository
            and not isinstance(self.repository, Unset)
            and not isinstance(self.repository, dict)
        ):
            repository = self.repository.to_dict()
        elif self.repository and isinstance(self.repository, dict):
            repository = self.repository

        revision: dict[str, Any] | Unset = UNSET
        if (
            self.revision
            and not isinstance(self.revision, Unset)
            and not isinstance(self.revision, dict)
        ):
            revision = self.revision.to_dict()
        elif self.revision and isinstance(self.revision, dict):
            revision = self.revision

        runtime: dict[str, Any] | Unset = UNSET
        if (
            self.runtime
            and not isinstance(self.runtime, Unset)
            and not isinstance(self.runtime, dict)
        ):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

        triggers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = []
            for componentsschemas_triggers_item_data in self.triggers:
                if type(componentsschemas_triggers_item_data) is dict:
                    componentsschemas_triggers_item = componentsschemas_triggers_item_data
                else:
                    componentsschemas_triggers_item = componentsschemas_triggers_item_data.to_dict()
                triggers.append(componentsschemas_triggers_item)

        volumes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.volumes, Unset):
            volumes = []
            for componentsschemas_volume_attachments_item_data in self.volumes:
                if type(componentsschemas_volume_attachments_item_data) is dict:
                    componentsschemas_volume_attachments_item = (
                        componentsschemas_volume_attachments_item_data
                    )
                else:
                    componentsschemas_volume_attachments_item = (
                        componentsschemas_volume_attachments_item_data.to_dict()
                    )
                volumes.append(componentsschemas_volume_attachments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if policies is not UNSET:
            field_dict["policies"] = policies
        if public is not UNSET:
            field_dict["public"] = public
        if region is not UNSET:
            field_dict["region"] = region
        if repository is not UNSET:
            field_dict["repository"] = repository
        if revision is not UNSET:
            field_dict["revision"] = revision
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if triggers is not UNSET:
            field_dict["triggers"] = triggers
        if volumes is not UNSET:
            field_dict["volumes"] = volumes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.agent_runtime import AgentRuntime  # noqa: PLC0415
        from ..models.repository import Repository  # noqa: PLC0415
        from ..models.revision_configuration import RevisionConfiguration  # noqa: PLC0415
        from ..models.trigger import Trigger  # noqa: PLC0415
        from ..models.volume_attachment import VolumeAttachment  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        policies = cast(list[str], d.pop("policies", UNSET))

        public = d.pop("public", UNSET)

        region = d.pop("region", UNSET)

        _repository = d.pop("repository", UNSET)
        repository: Repository | Unset
        if isinstance(_repository, Unset):
            repository = UNSET
        else:
            repository = Repository.from_dict(_repository)

        _revision = d.pop("revision", UNSET)
        revision: RevisionConfiguration | Unset
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = RevisionConfiguration.from_dict(_revision)

        _runtime = d.pop("runtime", UNSET)
        runtime: AgentRuntime | Unset
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

        volumes = []
        _volumes = d.pop("volumes", UNSET)
        for componentsschemas_volume_attachments_item_data in _volumes or []:
            componentsschemas_volume_attachments_item = VolumeAttachment.from_dict(
                componentsschemas_volume_attachments_item_data
            )

            volumes.append(componentsschemas_volume_attachments_item)

        agent_spec = cls(
            enabled=enabled,
            policies=policies,
            public=public,
            region=region,
            repository=repository,
            revision=revision,
            runtime=runtime,
            triggers=triggers,
            volumes=volumes,
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
