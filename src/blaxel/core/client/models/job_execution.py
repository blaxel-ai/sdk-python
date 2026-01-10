from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_execution_status import JobExecutionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_execution_metadata import JobExecutionMetadata
    from ..models.job_execution_spec import JobExecutionSpec
    from ..models.job_execution_stats import JobExecutionStats
    from ..models.job_execution_task import JobExecutionTask


T = TypeVar("T", bound="JobExecution")


@_attrs_define
class JobExecution:
    """Job execution

    Attributes:
        metadata (JobExecutionMetadata): Job execution metadata
        spec (JobExecutionSpec): Job execution specification
        stats (Union[Unset, JobExecutionStats]): Job execution statistics
        status (Union[Unset, JobExecutionStatus]): Job execution status
        tasks (Union[Unset, list['JobExecutionTask']]): List of execution tasks
    """

    metadata: "JobExecutionMetadata"
    spec: "JobExecutionSpec"
    stats: Union[Unset, "JobExecutionStats"] = UNSET
    status: Union[Unset, JobExecutionStatus] = UNSET
    tasks: Union[Unset, list["JobExecutionTask"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if type(self.metadata) is dict:
            metadata = self.metadata
        else:
            metadata = self.metadata.to_dict()

        if type(self.spec) is dict:
            spec = self.spec
        else:
            spec = self.spec.to_dict()

        stats: Union[Unset, dict[str, Any]] = UNSET
        if self.stats and not isinstance(self.stats, Unset) and not isinstance(self.stats, dict):
            stats = self.stats.to_dict()
        elif self.stats and isinstance(self.stats, dict):
            stats = self.stats

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        tasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = []
            for tasks_item_data in self.tasks:
                if type(tasks_item_data) is dict:
                    tasks_item = tasks_item_data
                else:
                    tasks_item = tasks_item_data.to_dict()
                tasks.append(tasks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "spec": spec,
            }
        )
        if stats is not UNSET:
            field_dict["stats"] = stats
        if status is not UNSET:
            field_dict["status"] = status
        if tasks is not UNSET:
            field_dict["tasks"] = tasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job_execution_metadata import JobExecutionMetadata
        from ..models.job_execution_spec import JobExecutionSpec
        from ..models.job_execution_stats import JobExecutionStats
        from ..models.job_execution_task import JobExecutionTask

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = JobExecutionMetadata.from_dict(d.pop("metadata"))

        spec = JobExecutionSpec.from_dict(d.pop("spec"))

        _stats = d.pop("stats", UNSET)
        stats: Union[Unset, JobExecutionStats]
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = JobExecutionStats.from_dict(_stats)

        _status = d.pop("status", UNSET)
        status: Union[Unset, JobExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = JobExecutionStatus(_status)

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = JobExecutionTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        job_execution = cls(
            metadata=metadata,
            spec=spec,
            stats=stats,
            status=status,
            tasks=tasks,
        )

        job_execution.additional_properties = d
        return job_execution

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
