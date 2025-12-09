from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_request_env import ProcessRequestEnv


T = TypeVar("T", bound="ProcessRequest")


@_attrs_define
class ProcessRequest:
    """
    Attributes:
        command (str):  Example: ls -la.
        env (Union[Unset, ProcessRequestEnv]):  Example: {'{"PORT"': ' "3000"}'}.
        max_restarts (Union[Unset, int]):  Example: 3.
        name (Union[Unset, str]):  Example: my-process.
        restart_on_failure (Union[Unset, bool]):  Example: True.
        timeout (Union[Unset, int]):  Example: 30.
        wait_for_completion (Union[Unset, bool]):
        wait_for_ports (Union[Unset, list[int]]):  Example: [3000, 8080].
        working_dir (Union[Unset, str]):  Example: /home/user.
    """

    command: str
    env: Union[Unset, "ProcessRequestEnv"] = UNSET
    max_restarts: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    restart_on_failure: Union[Unset, bool] = UNSET
    timeout: Union[Unset, int] = UNSET
    wait_for_completion: Union[Unset, bool] = UNSET
    wait_for_ports: Union[Unset, list[int]] = UNSET
    working_dir: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        env: Union[Unset, dict[str, Any]] = UNSET
        if self.env and not isinstance(self.env, Unset) and not isinstance(self.env, dict):
            env = self.env.to_dict()
        elif self.env and isinstance(self.env, dict):
            env = self.env

        max_restarts = self.max_restarts

        name = self.name

        restart_on_failure = self.restart_on_failure

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
        if env is not UNSET:
            field_dict["env"] = env
        if max_restarts is not UNSET:
            field_dict["maxRestarts"] = max_restarts
        if name is not UNSET:
            field_dict["name"] = name
        if restart_on_failure is not UNSET:
            field_dict["restartOnFailure"] = restart_on_failure
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.process_request_env import ProcessRequestEnv

        if not src_dict:
            return None
        d = src_dict.copy()
        command = d.pop("command")

        _env = d.pop("env", UNSET)
        env: Union[Unset, ProcessRequestEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = ProcessRequestEnv.from_dict(_env)

        max_restarts = d.pop("maxRestarts", d.pop("max_restarts", UNSET))

        name = d.pop("name", UNSET)

        restart_on_failure = d.pop("restartOnFailure", d.pop("restart_on_failure", UNSET))

        timeout = d.pop("timeout", UNSET)

        wait_for_completion = d.pop("waitForCompletion", d.pop("wait_for_completion", UNSET))

        wait_for_ports = cast(list[int], d.pop("waitForPorts", d.pop("wait_for_ports", UNSET)))

        working_dir = d.pop("workingDir", d.pop("working_dir", UNSET))

        process_request = cls(
            command=command,
            env=env,
            max_restarts=max_restarts,
            name=name,
            restart_on_failure=restart_on_failure,
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
