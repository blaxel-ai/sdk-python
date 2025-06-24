from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.process_response_status import ProcessResponseStatus

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
        working_dir (str):  Example: /home/user.
    """

    command: str
    completed_at: str
    exit_code: int
    logs: str
    name: str
    pid: str
    started_at: str
    status: ProcessResponseStatus
    working_dir: str
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

        working_dir = self.working_dir

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
                "workingDir": working_dir,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        command = d.pop("command")

        completed_at = d.pop("completedAt")

        exit_code = d.pop("exitCode")

        logs = d.pop("logs")

        name = d.pop("name")

        pid = d.pop("pid")

        started_at = d.pop("startedAt")

        status = ProcessResponseStatus(d.pop("status"))

        working_dir = d.pop("workingDir")

        process_response = cls(
            command=command,
            completed_at=completed_at,
            exit_code=exit_code,
            logs=logs,
            name=name,
            pid=pid,
            started_at=started_at,
            status=status,
            working_dir=working_dir,
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
