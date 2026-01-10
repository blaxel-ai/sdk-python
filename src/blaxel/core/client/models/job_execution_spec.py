from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_execution_task import JobExecutionTask


T = TypeVar("T", bound="JobExecutionSpec")


@_attrs_define
class JobExecutionSpec:
    """Job execution specification

    Attributes:
        parallelism (Union[Unset, int]): Number of parallel tasks Example: 5.
        tasks (Union[Unset, list['JobExecutionTask']]): List of execution tasks
        timeout (Union[Unset, int]): Job timeout in seconds (captured at execution creation time) Example: 3600.
    """

    parallelism: Union[Unset, int] = UNSET
    tasks: Union[Unset, list["JobExecutionTask"]] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job_execution_task import JobExecutionTask

        if not src_dict:
            return None
        d = src_dict.copy()
        parallelism = d.pop("parallelism", UNSET)

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = JobExecutionTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        timeout = d.pop("timeout", UNSET)

        job_execution_spec = cls(
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
