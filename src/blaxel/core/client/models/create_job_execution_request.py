from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_job_execution_request_env import CreateJobExecutionRequestEnv
    from ..models.create_job_execution_request_tasks_item import CreateJobExecutionRequestTasksItem


T = TypeVar("T", bound="CreateJobExecutionRequest")


@_attrs_define
class CreateJobExecutionRequest:
    """Request to create a job execution

    Attributes:
        allow_queue (bool | Unset): When false, capacity is checked synchronously and the request is rejected
            immediately with a 429 error if the execution cannot start right now, instead of being queued and retried in the
            background. No execution is created on rejection. Defaults to true (queue and retry).
        env (CreateJobExecutionRequestEnv | Unset): Environment variable overrides (optional, will merge with job's
            environment variables) Example: {"MY_VAR": "custom_value", "BATCH_SIZE": "100"}.
        execution_id (str | Unset): Execution ID (optional, will be generated if not provided)
        id (str | Unset): Unique message ID
        job_id (str | Unset): Job ID Example: data-processing-job.
        memory (int | Unset): Memory override in megabytes (optional, must be lower than or equal to job's configured
            memory) Example: 2048.
        tasks (list[CreateJobExecutionRequestTasksItem] | Unset): Array of task parameters for parallel execution
        workspace_id (str | Unset): Workspace ID
    """

    allow_queue: bool | Unset = UNSET
    env: CreateJobExecutionRequestEnv | Unset = UNSET
    execution_id: str | Unset = UNSET
    id: str | Unset = UNSET
    job_id: str | Unset = UNSET
    memory: int | Unset = UNSET
    tasks: list[CreateJobExecutionRequestTasksItem] | Unset = UNSET
    workspace_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allow_queue = self.allow_queue

        env: dict[str, Any] | Unset = UNSET
        if self.env and not isinstance(self.env, Unset) and not isinstance(self.env, dict):
            env = self.env.to_dict()
        elif self.env and isinstance(self.env, dict):
            env = self.env

        execution_id = self.execution_id

        id = self.id

        job_id = self.job_id

        memory = self.memory

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
        if allow_queue is not UNSET:
            field_dict["allowQueue"] = allow_queue
        if env is not UNSET:
            field_dict["env"] = env
        if execution_id is not UNSET:
            field_dict["executionId"] = execution_id
        if id is not UNSET:
            field_dict["id"] = id
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if memory is not UNSET:
            field_dict["memory"] = memory
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.create_job_execution_request_env import (
            CreateJobExecutionRequestEnv,  # noqa: PLC0415
        )
        from ..models.create_job_execution_request_tasks_item import (
            CreateJobExecutionRequestTasksItem,
        )  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        allow_queue = d.pop("allowQueue", d.pop("allow_queue", UNSET))

        _env = d.pop("env", UNSET)
        env: CreateJobExecutionRequestEnv | Unset
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = CreateJobExecutionRequestEnv.from_dict(_env)

        execution_id = d.pop("executionId", d.pop("execution_id", UNSET))

        id = d.pop("id", UNSET)

        job_id = d.pop("jobId", d.pop("job_id", UNSET))

        memory = d.pop("memory", UNSET)

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = CreateJobExecutionRequestTasksItem.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        workspace_id = d.pop("workspaceId", d.pop("workspace_id", UNSET))

        create_job_execution_request = cls(
            allow_queue=allow_queue,
            env=env,
            execution_id=execution_id,
            id=id,
            job_id=job_id,
            memory=memory,
            tasks=tasks,
            workspace_id=workspace_id,
        )

        create_job_execution_request.additional_properties = d
        return create_job_execution_request

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
