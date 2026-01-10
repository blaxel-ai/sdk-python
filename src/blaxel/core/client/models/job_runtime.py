from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_runtime_generation import JobRuntimeGeneration
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.env import Env
    from ..models.port import Port


T = TypeVar("T", bound="JobRuntime")


@_attrs_define
class JobRuntime:
    """Runtime configuration defining how batch job tasks are executed with parallelism and retry settings

    Attributes:
        envs (Union[Unset, list['Env']]): Environment variables injected into job tasks. Supports Kubernetes EnvVar
            format with valueFrom references.
        generation (Union[Unset, JobRuntimeGeneration]): Infrastructure generation: mk2 (containers, 2-10s cold starts)
            or mk3 (microVMs, sub-25ms cold starts) Example: mk3.
        image (Union[Unset, str]): Container image built by Blaxel when deploying with 'bl deploy'. This field is auto-
            populated during deployment.
        max_concurrent_tasks (Union[Unset, int]): Maximum number of tasks that can run simultaneously within a single
            execution Example: 10.
        max_retries (Union[Unset, int]): Number of automatic retry attempts for failed tasks before marking as failed
            Example: 3.
        memory (Union[Unset, int]): Memory allocation in megabytes. Also determines CPU allocation (CPU cores = memory
            in MB / 2048, e.g., 4096MB = 2 CPUs). Example: 2048.
        ports (Union[Unset, list['Port']]): Set of ports for a resource
        timeout (Union[Unset, int]): Maximum execution time in seconds before a task is terminated Example: 3600.
    """

    envs: Union[Unset, list["Env"]] = UNSET
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
        from ..models.env import Env
        from ..models.port import Port

        if not src_dict:
            return None
        d = src_dict.copy()
        envs = []
        _envs = d.pop("envs", UNSET)
        for envs_item_data in _envs or []:
            envs_item = Env.from_dict(envs_item_data)

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
