from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PolicyUsageCounts")


@_attrs_define
class PolicyUsageCounts:
    """Per-resource counts of how many resources reference a policy. Computed by the policies listing endpoint to avoid
    client-side fan-out across the agents/models/functions/sandboxes/jobs listings.

        Attributes:
            agents (Union[Unset, int]):
            functions (Union[Unset, int]):
            jobs (Union[Unset, int]):
            models (Union[Unset, int]):
            sandboxes (Union[Unset, int]):
    """

    agents: Union[Unset, int] = UNSET
    functions: Union[Unset, int] = UNSET
    jobs: Union[Unset, int] = UNSET
    models: Union[Unset, int] = UNSET
    sandboxes: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agents = self.agents

        functions = self.functions

        jobs = self.jobs

        models = self.models

        sandboxes = self.sandboxes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agents is not UNSET:
            field_dict["agents"] = agents
        if functions is not UNSET:
            field_dict["functions"] = functions
        if jobs is not UNSET:
            field_dict["jobs"] = jobs
        if models is not UNSET:
            field_dict["models"] = models
        if sandboxes is not UNSET:
            field_dict["sandboxes"] = sandboxes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        agents = d.pop("agents", UNSET)

        functions = d.pop("functions", UNSET)

        jobs = d.pop("jobs", UNSET)

        models = d.pop("models", UNSET)

        sandboxes = d.pop("sandboxes", UNSET)

        policy_usage_counts = cls(
            agents=agents,
            functions=functions,
            jobs=jobs,
            models=models,
            sandboxes=sandboxes,
        )

        policy_usage_counts.additional_properties = d
        return policy_usage_counts

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
