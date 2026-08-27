from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_schedule_execution_status import SandboxScheduleExecutionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxScheduleExecution")


@_attrs_define
class SandboxScheduleExecution:
    """One recorded execution of a sandbox schedule. status and statusCode describe whether the scheduler's process
    submission was accepted; the scheduler does not wait for the process to finish. Stored in the dedicated
    scheduleexecutions table.

        Attributes:
            created_at (Union[Unset, str]): Creation timestamp (read-only).
            error (Union[Unset, str]): Reason the execution failed, naming the resource that could not be reached. Empty
                when the command was accepted by the sandbox. Example: sandbox my-sandbox is not reachable at https://xxx.us-
                pdx-1.bl.run (HTTP 404).
            executed_at (Union[Unset, str]): RFC 3339 time at which the command was submitted. Example:
                2026-07-01T09:00:00Z.
            id (Union[Unset, str]): Unique id of this execution within the schedule. Example: 00000000000000000042.
            process_name (Union[Unset, str]): Name of the process started in the sandbox for this execution, used to look up
                its logs. Example: training-job.
            sandbox (Union[Unset, str]): Name of the sandbox this execution belongs to.
            schedule_id (Union[Unset, str]): Id of the schedule this execution belongs to. Example: schedule-0.
            status (Union[Unset, SandboxScheduleExecutionStatus]): Whether submitting the process request was accepted. This
                is not the process completion status.
            status_code (Union[Unset, int]): HTTP status code returned when the scheduled command was submitted to the
                sandbox (0 if the sandbox could not be reached). 2xx/3xx means the command was accepted. Example: 200.
            timeout (Union[Unset, int]): Process timeout in seconds for this execution. The UI uses it to scope the log view
                to [executedAt, executedAt+timeout]. 0 when the schedule set no timeout. Example: 600.
    """

    created_at: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    executed_at: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    process_name: Union[Unset, str] = UNSET
    sandbox: Union[Unset, str] = UNSET
    schedule_id: Union[Unset, str] = UNSET
    status: Union[Unset, SandboxScheduleExecutionStatus] = UNSET
    status_code: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        error = self.error

        executed_at = self.executed_at

        id = self.id

        process_name = self.process_name

        sandbox = self.sandbox

        schedule_id = self.schedule_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_code = self.status_code

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if error is not UNSET:
            field_dict["error"] = error
        if executed_at is not UNSET:
            field_dict["executedAt"] = executed_at
        if id is not UNSET:
            field_dict["id"] = id
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox
        if schedule_id is not UNSET:
            field_dict["scheduleId"] = schedule_id
        if status is not UNSET:
            field_dict["status"] = status
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        error = d.pop("error", UNSET)

        executed_at = d.pop("executedAt", d.pop("executed_at", UNSET))

        id = d.pop("id", UNSET)

        process_name = d.pop("processName", d.pop("process_name", UNSET))

        sandbox = d.pop("sandbox", UNSET)

        schedule_id = d.pop("scheduleId", d.pop("schedule_id", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, SandboxScheduleExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SandboxScheduleExecutionStatus(_status)

        status_code = d.pop("statusCode", d.pop("status_code", UNSET))

        timeout = d.pop("timeout", UNSET)

        sandbox_schedule_execution = cls(
            created_at=created_at,
            error=error,
            executed_at=executed_at,
            id=id,
            process_name=process_name,
            sandbox=sandbox,
            schedule_id=schedule_id,
            status=status,
            status_code=status_code,
            timeout=timeout,
        )

        sandbox_schedule_execution.additional_properties = d
        return sandbox_schedule_execution

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
