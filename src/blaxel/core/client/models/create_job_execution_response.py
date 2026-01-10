from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_job_execution_response_tasks_item import (
        CreateJobExecutionResponseTasksItem,
    )


T = TypeVar("T", bound="CreateJobExecutionResponse")


@_attrs_define
class CreateJobExecutionResponse:
    """Response returned when a job execution is successfully created. Contains identifiers and the tasks that will be
    executed.

        Attributes:
            execution_id (Union[Unset, str]): Unique identifier for the created execution. Use this ID to track execution
                status, retrieve logs, or cancel the execution. Example: exec-abc123.
            id (Union[Unset, str]): Unique identifier for this request, used for idempotency and tracking. Auto-generated if
                not provided in the request. Example: 550e8400-e29b-41d4-a716-446655440000.
            job_id (Union[Unset, str]): Name of the job that this execution belongs to Example: data-processing-job.
            tasks (Union[Unset, list['CreateJobExecutionResponseTasksItem']]): Array of task configurations that will be
                executed in parallel according to the job's concurrency settings. Each task can have custom parameters.
            workspace_id (Union[Unset, str]): Name of the workspace where the job execution was created Example: my-
                workspace.
    """

    execution_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    job_id: Union[Unset, str] = UNSET
    tasks: Union[Unset, list["CreateJobExecutionResponseTasksItem"]] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_id = self.execution_id

        id = self.id

        job_id = self.job_id

        tasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = []
            for tasks_item_data in self.tasks:
                if type(tasks_item_data) is dict:
                    tasks_item = tasks_item_data
                else:
                    tasks_item = tasks_item_data.to_dict()
                tasks.append(tasks_item)

        workspace_id = self.workspace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if execution_id is not UNSET:
            field_dict["executionId"] = execution_id
        if id is not UNSET:
            field_dict["id"] = id
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.create_job_execution_response_tasks_item import (
            CreateJobExecutionResponseTasksItem,
        )

        if not src_dict:
            return None
        d = src_dict.copy()
        execution_id = d.pop("executionId", d.pop("execution_id", UNSET))

        id = d.pop("id", UNSET)

        job_id = d.pop("jobId", d.pop("job_id", UNSET))

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = CreateJobExecutionResponseTasksItem.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        workspace_id = d.pop("workspaceId", d.pop("workspace_id", UNSET))

        create_job_execution_response = cls(
            execution_id=execution_id,
            id=id,
            job_id=job_id,
            tasks=tasks,
            workspace_id=workspace_id,
        )

        create_job_execution_response.additional_properties = d
        return create_job_execution_response

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
