from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessLogs")


@_attrs_define
class ProcessLogs:
    """
    Attributes:
        logs (Union[Unset, str]):  Example: logs output.
        stderr (Union[Unset, str]):  Example: stderr output.
        stdout (Union[Unset, str]):  Example: stdout output.
    """

    logs: Union[Unset, str] = UNSET
    stderr: Union[Unset, str] = UNSET
    stdout: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logs = self.logs

        stderr = self.stderr

        stdout = self.stdout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if logs is not UNSET:
            field_dict["logs"] = logs
        if stderr is not UNSET:
            field_dict["stderr"] = stderr
        if stdout is not UNSET:
            field_dict["stdout"] = stdout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        logs = d.pop("logs", UNSET)

        stderr = d.pop("stderr", UNSET)

        stdout = d.pop("stdout", UNSET)

        process_logs = cls(
            logs=logs,
            stderr=stderr,
            stdout=stdout,
        )

        process_logs.additional_properties = d
        return process_logs

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
