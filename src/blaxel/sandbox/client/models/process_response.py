from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessResponse")


@_attrs_define
class ProcessResponse:
    """
    Attributes:
        command (Union[Unset, str]):  Example: ls -la.
        completed_at (Union[Unset, str]):  Example: Wed, 01 Jan 2023 12:01:00 GMT.
        exit_code (Union[Unset, int]):
        name (Union[Unset, str]):  Example: my-process.
        pid (Union[Unset, str]):  Example: 1234.
        started_at (Union[Unset, str]):  Example: Wed, 01 Jan 2023 12:00:00 GMT.
        status (Union[Unset, str]):  Example: running.
        working_dir (Union[Unset, str]):  Example: /home/user.
    """

    command: Union[Unset, str] = UNSET
    completed_at: Union[Unset, str] = UNSET
    exit_code: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    pid: Union[Unset, str] = UNSET
    started_at: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    working_dir: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        completed_at = self.completed_at

        exit_code = self.exit_code

        name = self.name

        pid = self.pid

        started_at = self.started_at

        status = self.status

        working_dir = self.working_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["command"] = command
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if exit_code is not UNSET:
            field_dict["exitCode"] = exit_code
        if name is not UNSET:
            field_dict["name"] = name
        if pid is not UNSET:
            field_dict["pid"] = pid
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if status is not UNSET:
            field_dict["status"] = status
        if working_dir is not UNSET:
            field_dict["workingDir"] = working_dir

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        command = d.pop("command", UNSET)

        completed_at = d.pop("completedAt", UNSET)

        exit_code = d.pop("exitCode", UNSET)

        name = d.pop("name", UNSET)

        pid = d.pop("pid", UNSET)

        started_at = d.pop("startedAt", UNSET)

        status = d.pop("status", UNSET)

        working_dir = d.pop("workingDir", UNSET)

        process_response = cls(
            command=command,
            completed_at=completed_at,
            exit_code=exit_code,
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
