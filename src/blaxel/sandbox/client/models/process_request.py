from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessRequest")


@_attrs_define
class ProcessRequest:
    """
    Attributes:
        command (str):  Example: ls -la.
        name (Union[Unset, str]):  Example: my-process.
        stream_logs (Union[Unset, bool]):  Example: True.
        timeout (Union[Unset, int]):  Example: 30.
        wait_for_completion (Union[Unset, bool]):
        wait_for_ports (Union[Unset, list[int]]):  Example: [3000, 8080].
        working_dir (Union[Unset, str]):  Example: /home/user.
    """

    command: str
    name: Union[Unset, str] = UNSET
    stream_logs: Union[Unset, bool] = UNSET
    timeout: Union[Unset, int] = UNSET
    wait_for_completion: Union[Unset, bool] = UNSET
    wait_for_ports: Union[Unset, list[int]] = UNSET
    working_dir: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        name = self.name

        stream_logs = self.stream_logs

        timeout = self.timeout

        wait_for_completion = self.wait_for_completion

        wait_for_ports: Union[Unset, list[int]] = UNSET
        if not isinstance(self.wait_for_ports, Unset):
            wait_for_ports = self.wait_for_ports

        working_dir = self.working_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command": command,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if stream_logs is not UNSET:
            field_dict["streamLogs"] = stream_logs
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if wait_for_completion is not UNSET:
            field_dict["waitForCompletion"] = wait_for_completion
        if wait_for_ports is not UNSET:
            field_dict["waitForPorts"] = wait_for_ports
        if working_dir is not UNSET:
            field_dict["workingDir"] = working_dir

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        command = d.pop("command")

        name = d.pop("name", UNSET)

        stream_logs = d.pop("streamLogs", UNSET)

        timeout = d.pop("timeout", UNSET)

        wait_for_completion = d.pop("waitForCompletion", UNSET)

        wait_for_ports = cast(list[int], d.pop("waitForPorts", UNSET))

        working_dir = d.pop("workingDir", UNSET)

        process_request = cls(
            command=command,
            name=name,
            stream_logs=stream_logs,
            timeout=timeout,
            wait_for_completion=wait_for_completion,
            wait_for_ports=wait_for_ports,
            working_dir=working_dir,
        )

        process_request.additional_properties = d
        return process_request

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
