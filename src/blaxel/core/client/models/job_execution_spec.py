from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_execution_spec_env_override import JobExecutionSpecEnvOverride
    from ..models.job_execution_task import JobExecutionTask


T = TypeVar("T", bound="JobExecutionSpec")


@_attrs_define
class JobExecutionSpec:
    """Job execution specification

    Attributes:
        env_override (Union[Unset, JobExecutionSpecEnvOverride]): Environment variable overrides (if provided for this
            execution, values are masked with ***) Example: {"MY_VAR": "***", "BATCH_SIZE": "***"}.
        memory_override (Union[Unset, int]): Memory override in megabytes (if provided for this execution) Example:
            2048.
        parallelism (Union[Unset, int]): Number of parallel tasks Example: 5.
        tasks (Union[Unset, list['JobExecutionTask']]): List of execution tasks
        timeout (Union[Unset, int]): Job timeout in seconds (captured at execution creation time) Example: 3600.
    """

    env_override: Union[Unset, "JobExecutionSpecEnvOverride"] = UNSET
    memory_override: Union[Unset, int] = UNSET
    parallelism: Union[Unset, int] = UNSET
    tasks: Union[Unset, list["JobExecutionTask"]] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        env_override: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.env_override
            and not isinstance(self.env_override, Unset)
            and not isinstance(self.env_override, dict)
        ):
            env_override = self.env_override.to_dict()
        elif self.env_override and isinstance(self.env_override, dict):
            env_override = self.env_override

        memory_override = self.memory_override

        parallelism = self.parallelism

        tasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = []
            for tasks_item_data in self.tasks:
                if type(tasks_item_data) is dict:
                    tasks_item = tasks_item_data
                else:
                    tasks_item = tasks_item_data.to_dict()
                tasks.append(tasks_item)

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if env_override is not UNSET:
            field_dict["envOverride"] = env_override
        if memory_override is not UNSET:
            field_dict["memoryOverride"] = memory_override
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job_execution_spec_env_override import JobExecutionSpecEnvOverride
        from ..models.job_execution_task import JobExecutionTask

        if not src_dict:
            return None
        d = src_dict.copy()
        _env_override = d.pop("envOverride", d.pop("env_override", UNSET))
        env_override: Union[Unset, JobExecutionSpecEnvOverride]
        if isinstance(_env_override, Unset):
            env_override = UNSET
        else:
            env_override = JobExecutionSpecEnvOverride.from_dict(_env_override)

        memory_override = d.pop("memoryOverride", d.pop("memory_override", UNSET))

        parallelism = d.pop("parallelism", UNSET)

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = JobExecutionTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        timeout = d.pop("timeout", UNSET)

        job_execution_spec = cls(
            env_override=env_override,
            memory_override=memory_override,
            parallelism=parallelism,
            tasks=tasks,
            timeout=timeout,
        )

        job_execution_spec.additional_properties = d
        return job_execution_spec

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
