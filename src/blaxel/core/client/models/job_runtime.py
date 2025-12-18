from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_runtime_generation import JobRuntimeGeneration
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_runtime_envs_item import JobRuntimeEnvsItem
    from ..models.port import Port


T = TypeVar("T", bound="JobRuntime")


@_attrs_define
class JobRuntime:
    """Runtime configuration for Job

    Attributes:
        envs (Union[Unset, list['JobRuntimeEnvsItem']]): The env variables to set in the job. Should be a list of
            Kubernetes EnvVar types
        generation (Union[Unset, JobRuntimeGeneration]): The generation of the job
        image (Union[Unset, str]): The Docker image for the job
        max_concurrent_tasks (Union[Unset, int]): The maximum number of concurrent task for an execution
        max_retries (Union[Unset, int]): The maximum number of retries for the job
        memory (Union[Unset, int]): The memory for the job in MB
        ports (Union[Unset, list['Port']]): Set of ports for a resource
        timeout (Union[Unset, int]): The timeout for the job in seconds
    """

    envs: Union[Unset, list["JobRuntimeEnvsItem"]] = UNSET
    generation: Union[Unset, JobRuntimeGeneration] = UNSET
    image: Union[Unset, str] = UNSET
    max_concurrent_tasks: Union[Unset, int] = UNSET
    max_retries: Union[Unset, int] = UNSET
    memory: Union[Unset, int] = UNSET
    ports: Union[Unset, list["Port"]] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        envs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = []
            for envs_item_data in self.envs:
                if type(envs_item_data) is dict:
                    envs_item = envs_item_data
                else:
                    envs_item = envs_item_data.to_dict()
                envs.append(envs_item)

        generation: Union[Unset, str] = UNSET
        if not isinstance(self.generation, Unset):
            generation = self.generation.value

        image = self.image

        max_concurrent_tasks = self.max_concurrent_tasks

        max_retries = self.max_retries

        memory = self.memory

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for componentsschemas_ports_item_data in self.ports:
                if type(componentsschemas_ports_item_data) is dict:
                    componentsschemas_ports_item = componentsschemas_ports_item_data
                else:
                    componentsschemas_ports_item = componentsschemas_ports_item_data.to_dict()
                ports.append(componentsschemas_ports_item)

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if envs is not UNSET:
            field_dict["envs"] = envs
        if generation is not UNSET:
            field_dict["generation"] = generation
        if image is not UNSET:
            field_dict["image"] = image
        if max_concurrent_tasks is not UNSET:
            field_dict["maxConcurrentTasks"] = max_concurrent_tasks
        if max_retries is not UNSET:
            field_dict["maxRetries"] = max_retries
        if memory is not UNSET:
            field_dict["memory"] = memory
        if ports is not UNSET:
            field_dict["ports"] = ports
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job_runtime_envs_item import JobRuntimeEnvsItem
        from ..models.port import Port

        if not src_dict:
            return None
        d = src_dict.copy()
        envs = []
        _envs = d.pop("envs", UNSET)
        for envs_item_data in _envs or []:
            envs_item = JobRuntimeEnvsItem.from_dict(envs_item_data)

            envs.append(envs_item)

        _generation = d.pop("generation", UNSET)
        generation: Union[Unset, JobRuntimeGeneration]
        if isinstance(_generation, Unset):
            generation = UNSET
        else:
            generation = JobRuntimeGeneration(_generation)

        image = d.pop("image", UNSET)

        max_concurrent_tasks = d.pop("maxConcurrentTasks", d.pop("max_concurrent_tasks", UNSET))

        max_retries = d.pop("maxRetries", d.pop("max_retries", UNSET))

        memory = d.pop("memory", UNSET)

        ports = []
        _ports = d.pop("ports", UNSET)
        for componentsschemas_ports_item_data in _ports or []:
            componentsschemas_ports_item = Port.from_dict(componentsschemas_ports_item_data)

            ports.append(componentsschemas_ports_item)

        timeout = d.pop("timeout", UNSET)

        job_runtime = cls(
            envs=envs,
            generation=generation,
            image=image,
            max_concurrent_tasks=max_concurrent_tasks,
            max_retries=max_retries,
            memory=memory,
            ports=ports,
            timeout=timeout,
        )

        job_runtime.additional_properties = d
        return job_runtime

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
