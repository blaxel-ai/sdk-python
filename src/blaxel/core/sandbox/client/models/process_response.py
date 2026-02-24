from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.process_response_status import ProcessResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessResponse")


@_attrs_define
class ProcessResponse:
    """
    Attributes:
        command (str):  Example: ls -la.
        completed_at (str):  Example: Wed, 01 Jan 2023 12:01:00 GMT.
        exit_code (int):
        logs (str):  Example: logs output.
        name (str):  Example: my-process.
        pid (str):  Example: 1234.
        started_at (str):  Example: Wed, 01 Jan 2023 12:00:00 GMT.
        status (ProcessResponseStatus):  Example: running.
        stderr (str):  Example: stderr output.
        stdout (str):  Example: stdout output.
        working_dir (str):  Example: /home/user.
        max_restarts (Union[Unset, int]):  Example: 3.
        restart_count (Union[Unset, int]):  Example: 2.
        restart_on_failure (Union[Unset, bool]):  Example: True.
    """

    command: str
    completed_at: str
    exit_code: int
    logs: str
    name: str
    pid: str
    started_at: str
    status: ProcessResponseStatus
    stderr: str
    stdout: str
    working_dir: str
    max_restarts: Union[Unset, int] = UNSET
    restart_count: Union[Unset, int] = UNSET
    restart_on_failure: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        completed_at = self.completed_at

        exit_code = self.exit_code

        logs = self.logs

        name = self.name

        pid = self.pid

        started_at = self.started_at

        status = self.status.value

        stderr = self.stderr

        stdout = self.stdout

        working_dir = self.working_dir

        max_restarts = self.max_restarts

        restart_count = self.restart_count

        restart_on_failure = self.restart_on_failure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command": command,
                "completedAt": completed_at,
                "exitCode": exit_code,
                "logs": logs,
                "name": name,
                "pid": pid,
                "startedAt": started_at,
                "status": status,
                "stderr": stderr,
                "stdout": stdout,
                "workingDir": working_dir,
            }
        )
        if max_restarts is not UNSET:
            field_dict["maxRestarts"] = max_restarts
        if restart_count is not UNSET:
            field_dict["restartCount"] = restart_count
        if restart_on_failure is not UNSET:
            field_dict["restartOnFailure"] = restart_on_failure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        command = d.pop("command")

        completed_at = d.pop("completedAt") if "completedAt" in d else d.pop("completed_at")

        exit_code = d.pop("exitCode") if "exitCode" in d else d.pop("exit_code")

        logs = d.pop("logs")

        name = d.pop("name")

        pid = d.pop("pid")

        started_at = d.pop("startedAt") if "startedAt" in d else d.pop("started_at")

        status = ProcessResponseStatus(d.pop("status"))

        stderr = d.pop("stderr")

        stdout = d.pop("stdout")

        working_dir = d.pop("workingDir") if "workingDir" in d else d.pop("working_dir")

        max_restarts = d.pop("maxRestarts", d.pop("max_restarts", UNSET))

        restart_count = d.pop("restartCount", d.pop("restart_count", UNSET))

        restart_on_failure = d.pop("restartOnFailure", d.pop("restart_on_failure", UNSET))

        process_response = cls(
            command=command,
            completed_at=completed_at,
            exit_code=exit_code,
            logs=logs,
            name=name,
            pid=pid,
            started_at=started_at,
            status=status,
            stderr=stderr,
            stdout=stdout,
            working_dir=working_dir,
            max_restarts=max_restarts,
            restart_count=restart_count,
            restart_on_failure=restart_on_failure,
        )

        process_response.additional_properties = d
        return process_response

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
