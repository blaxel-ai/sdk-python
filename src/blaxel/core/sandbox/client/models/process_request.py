from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
        env (ProcessRequestEnv | Unset):  Example: {'{"PORT"': ' "3000"}'}.
        keep_alive (bool | Unset): Disable scale-to-zero while process runs. Default timeout is 600s (10 minutes). Set
            timeout to 0 for infinite. Example: False.
        max_restarts (int | Unset): Maximum number of restarts on failure. Set to a negative value (e.g. -1) for
            unlimited restarts. Example: 3.
        name (str | Unset):  Example: my-process.
        restart_on_failure (bool | Unset):  Example: True.
        stdin (bool | Unset): Open a writable stdin pipe, fed via POST /process/{identifier}/stdin and closed via
            DELETE. The pipe does not survive a sandbox-api restart: the process then sees EOF. Example: False.
        timeout (int | Unset): Timeout in seconds. When keepAlive is true, defaults to 600s (10 minutes). Set to 0 for
            infinite (no auto-kill). Example: 30.
        wait_for_completion (bool | Unset):  Example: False.
        wait_for_ports (list[int] | Unset):  Example: [3000, 8080].
        working_dir (str | Unset):  Example: /home/user.
    """

    command: str
    env: ProcessRequestEnv | Unset = UNSET
    keep_alive: bool | Unset = UNSET
    max_restarts: int | Unset = UNSET
    name: str | Unset = UNSET
    restart_on_failure: bool | Unset = UNSET
    stdin: bool | Unset = UNSET
    timeout: int | Unset = UNSET
    wait_for_completion: bool | Unset = UNSET
    wait_for_ports: list[int] | Unset = UNSET
    working_dir: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        env: dict[str, Any] | Unset = UNSET
        if self.env and not isinstance(self.env, Unset) and not isinstance(self.env, dict):
            env = self.env.to_dict()
        elif self.env and isinstance(self.env, dict):
            env = self.env

        keep_alive = self.keep_alive

        max_restarts = self.max_restarts

        name = self.name

        restart_on_failure = self.restart_on_failure

        stdin = self.stdin

        timeout = self.timeout

        wait_for_completion = self.wait_for_completion

        wait_for_ports: list[int] | Unset = UNSET
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
        if keep_alive is not UNSET:
            field_dict["keepAlive"] = keep_alive
        if max_restarts is not UNSET:
            field_dict["maxRestarts"] = max_restarts
        if name is not UNSET:
            field_dict["name"] = name
        if restart_on_failure is not UNSET:
            field_dict["restartOnFailure"] = restart_on_failure
        if stdin is not UNSET:
            field_dict["stdin"] = stdin
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.process_request_env import ProcessRequestEnv  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        command = d.pop("command")

        _env = d.pop("env", UNSET)
        env: ProcessRequestEnv | Unset
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = ProcessRequestEnv.from_dict(_env)

        keep_alive = d.pop("keepAlive", d.pop("keep_alive", UNSET))

        max_restarts = d.pop("maxRestarts", d.pop("max_restarts", UNSET))

        name = d.pop("name", UNSET)

        restart_on_failure = d.pop("restartOnFailure", d.pop("restart_on_failure", UNSET))

        stdin = d.pop("stdin", UNSET)

        timeout = d.pop("timeout", UNSET)

        wait_for_completion = d.pop("waitForCompletion", d.pop("wait_for_completion", UNSET))

        wait_for_ports = cast(list[int], d.pop("waitForPorts", d.pop("wait_for_ports", UNSET)))

        working_dir = d.pop("workingDir", d.pop("working_dir", UNSET))

        process_request = cls(
            command=command,
            env=env,
            keep_alive=keep_alive,
            max_restarts=max_restarts,
            name=name,
            restart_on_failure=restart_on_failure,
            stdin=stdin,
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
