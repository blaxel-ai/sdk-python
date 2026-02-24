from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_runtime import JobRuntime
    from ..models.revision_configuration import RevisionConfiguration
    from ..models.trigger import Trigger


T = TypeVar("T", bound="JobSpec")


@_attrs_define
class JobSpec:
    """Configuration for a batch job including execution parameters, parallelism settings, and deployment region

    Attributes:
        enabled (Union[Unset, bool]): When false, the job is disabled and new executions cannot be triggered Default:
            True. Example: True.
        policies (Union[Unset, list[str]]):
        region (Union[Unset, str]): Region where the job should be created (e.g. us-was-1, eu-lon-1) Example: us-was-1.
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, JobRuntime]): Runtime configuration defining how batch job tasks are executed with
            parallelism and retry settings
        triggers (Union[Unset, list['Trigger']]): Triggers to use your agent
    """

    enabled: Union[Unset, bool] = True
    policies: Union[Unset, list[str]] = UNSET
    region: Union[Unset, str] = UNSET
    revision: Union[Unset, "RevisionConfiguration"] = UNSET
    runtime: Union[Unset, "JobRuntime"] = UNSET
    triggers: Union[Unset, list["Trigger"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        policies: Union[Unset, list[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        region = self.region

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
        if region is not UNSET:
            field_dict["region"] = region
        if revision is not UNSET:
            field_dict["revision"] = revision
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job_runtime import JobRuntime
        from ..models.revision_configuration import RevisionConfiguration
        from ..models.trigger import Trigger

        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        policies = cast(list[str], d.pop("policies", UNSET))

        region = d.pop("region", UNSET)

        _revision = d.pop("revision", UNSET)
        revision: Union[Unset, RevisionConfiguration]
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = RevisionConfiguration.from_dict(_revision)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, JobRuntime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = JobRuntime.from_dict(_runtime)

        triggers = []
        _triggers = d.pop("triggers", UNSET)
        for componentsschemas_triggers_item_data in _triggers or []:
            componentsschemas_triggers_item = Trigger.from_dict(
                componentsschemas_triggers_item_data
            )

            triggers.append(componentsschemas_triggers_item)

        job_spec = cls(
            enabled=enabled,
            policies=policies,
            region=region,
            revision=revision,
            runtime=runtime,
            triggers=triggers,
        )

        job_spec.additional_properties = d
        return job_spec

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
