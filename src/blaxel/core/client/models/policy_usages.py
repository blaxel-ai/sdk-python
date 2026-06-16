from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.policy_usages_agents_item import PolicyUsagesAgentsItem
    from ..models.policy_usages_functions_item import PolicyUsagesFunctionsItem
    from ..models.policy_usages_jobs_item import PolicyUsagesJobsItem
    from ..models.policy_usages_models_item import PolicyUsagesModelsItem
    from ..models.policy_usages_sandboxes_item import PolicyUsagesSandboxesItem


T = TypeVar("T", bound="PolicyUsages")


@_attrs_define
class PolicyUsages:
    """Resources currently referencing a policy. Returned by GET /policies/{name}/usages so the policies UI can render
    attachments without fetching the agents/models/functions listings full.

        Attributes:
            agents (Union[Unset, list['PolicyUsagesAgentsItem']]): Names of agents whose spec.policies contains this policy.
            functions (Union[Unset, list['PolicyUsagesFunctionsItem']]): Names of functions whose spec.policies contains
                this policy.
            jobs (Union[Unset, list['PolicyUsagesJobsItem']]): Names of jobs whose spec.policies contains this policy.
            models (Union[Unset, list['PolicyUsagesModelsItem']]): Names of models whose spec.policies contains this policy.
            sandboxes (Union[Unset, list['PolicyUsagesSandboxesItem']]): Names of sandboxes whose spec.policies contains
                this policy.
    """

    agents: Union[Unset, list["PolicyUsagesAgentsItem"]] = UNSET
    functions: Union[Unset, list["PolicyUsagesFunctionsItem"]] = UNSET
    jobs: Union[Unset, list["PolicyUsagesJobsItem"]] = UNSET
    models: Union[Unset, list["PolicyUsagesModelsItem"]] = UNSET
    sandboxes: Union[Unset, list["PolicyUsagesSandboxesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        agents: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.agents, Unset):
            agents = []
            for agents_item_data in self.agents:
                if type(agents_item_data) is dict:
                    agents_item = agents_item_data
                else:
                    agents_item = agents_item_data.to_dict()
                agents.append(agents_item)

        functions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.functions, Unset):
            functions = []
            for functions_item_data in self.functions:
                if type(functions_item_data) is dict:
                    functions_item = functions_item_data
                else:
                    functions_item = functions_item_data.to_dict()
                functions.append(functions_item)

        jobs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.jobs, Unset):
            jobs = []
            for jobs_item_data in self.jobs:
                if type(jobs_item_data) is dict:
                    jobs_item = jobs_item_data
                else:
                    jobs_item = jobs_item_data.to_dict()
                jobs.append(jobs_item)

        models: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                if type(models_item_data) is dict:
                    models_item = models_item_data
                else:
                    models_item = models_item_data.to_dict()
                models.append(models_item)

        sandboxes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sandboxes, Unset):
            sandboxes = []
            for sandboxes_item_data in self.sandboxes:
                if type(sandboxes_item_data) is dict:
                    sandboxes_item = sandboxes_item_data
                else:
                    sandboxes_item = sandboxes_item_data.to_dict()
                sandboxes.append(sandboxes_item)

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
        from ..models.policy_usages_agents_item import PolicyUsagesAgentsItem
        from ..models.policy_usages_functions_item import PolicyUsagesFunctionsItem
        from ..models.policy_usages_jobs_item import PolicyUsagesJobsItem
        from ..models.policy_usages_models_item import PolicyUsagesModelsItem
        from ..models.policy_usages_sandboxes_item import PolicyUsagesSandboxesItem

        if not src_dict:
            return None
        d = src_dict.copy()
        agents = []
        _agents = d.pop("agents", UNSET)
        for agents_item_data in _agents or []:
            agents_item = PolicyUsagesAgentsItem.from_dict(agents_item_data)

            agents.append(agents_item)

        functions = []
        _functions = d.pop("functions", UNSET)
        for functions_item_data in _functions or []:
            functions_item = PolicyUsagesFunctionsItem.from_dict(functions_item_data)

            functions.append(functions_item)

        jobs = []
        _jobs = d.pop("jobs", UNSET)
        for jobs_item_data in _jobs or []:
            jobs_item = PolicyUsagesJobsItem.from_dict(jobs_item_data)

            jobs.append(jobs_item)

        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in _models or []:
            models_item = PolicyUsagesModelsItem.from_dict(models_item_data)

            models.append(models_item)

        sandboxes = []
        _sandboxes = d.pop("sandboxes", UNSET)
        for sandboxes_item_data in _sandboxes or []:
            sandboxes_item = PolicyUsagesSandboxesItem.from_dict(sandboxes_item_data)

            sandboxes.append(sandboxes_item)

        policy_usages = cls(
            agents=agents,
            functions=functions,
            jobs=jobs,
            models=models,
            sandboxes=sandboxes,
        )

        policy_usages.additional_properties = d
        return policy_usages

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
