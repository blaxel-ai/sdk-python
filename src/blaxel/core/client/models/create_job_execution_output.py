from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_job_execution_output_tasks_item import CreateJobExecutionOutputTasksItem


T = TypeVar("T", bound="CreateJobExecutionOutput")


@_attrs_define
class CreateJobExecutionOutput:
    """Response returned when a job execution is successfully created. Contains identifiers and the tasks that will be
    executed.

        Attributes:
            execution_id (str | Unset): Unique identifier for the created execution. Use this ID to track execution status,
                retrieve logs, or cancel the execution. Example: exec-abc123.
            id (str | Unset): Unique identifier for this request, used for idempotency and tracking. Auto-generated if not
                provided in the request. Example: 550e8400-e29b-41d4-a716-446655440000.
            job_id (str | Unset): Name of the job that this execution belongs to Example: data-processing-job.
            tasks (list[CreateJobExecutionOutputTasksItem] | Unset): Array of task configurations that will be executed in
                parallel according to the job's concurrency settings. Each task can have custom parameters.
            workspace_id (str | Unset): Name of the workspace where the job execution was created Example: my-workspace.
    """

    execution_id: str | Unset = UNSET
    id: str | Unset = UNSET
    job_id: str | Unset = UNSET
    tasks: list[CreateJobExecutionOutputTasksItem] | Unset = UNSET
    workspace_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_id = self.execution_id

        id = self.id

        job_id = self.job_id

        tasks: list[dict[str, Any]] | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.create_job_execution_output_tasks_item import (
            CreateJobExecutionOutputTasksItem,
        )  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        execution_id = d.pop("executionId", d.pop("execution_id", UNSET))

        id = d.pop("id", UNSET)

        job_id = d.pop("jobId", d.pop("job_id", UNSET))

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = CreateJobExecutionOutputTasksItem.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        workspace_id = d.pop("workspaceId", d.pop("workspace_id", UNSET))

        create_job_execution_output = cls(
            execution_id=execution_id,
            id=id,
            job_id=job_id,
            tasks=tasks,
            workspace_id=workspace_id,
        )

        create_job_execution_output.additional_properties = d
        return create_job_execution_output

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
