from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_schedule_input_env import SandboxScheduleInputEnv


T = TypeVar("T", bound="SandboxScheduleInput")


@_attrs_define
class SandboxScheduleInput:
    """Process execution configuration for a scheduled sandbox task

    Attributes:
        command (Union[Unset, str]): Shell command to execute inside the sandbox Example: python train.py --epochs 10.
        env (Union[Unset, SandboxScheduleInputEnv]): Environment variables to set for the process. May contain secrets,
            so values are encrypted at rest and masked in API responses unless an admin requests show_secrets=true.
        keep_alive (Union[Unset, bool]): Keep the sandbox alive (disable scale-to-zero) while the process runs. Defaults
            to true. Example: True.
        name (Union[Unset, str]): Optional name for the process (used to retrieve status/logs) Example: training-job.
        timeout (Union[Unset, int]): Timeout in seconds for the process. Defaults to 600 (10 minutes). Set to 0 for no
            timeout. Example: 3600.
        working_dir (Union[Unset, str]): Working directory for the command Example: /app.
    """

    command: Union[Unset, str] = UNSET
    env: Union[Unset, "SandboxScheduleInputEnv"] = UNSET
    keep_alive: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    timeout: Union[Unset, int] = UNSET
    working_dir: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        command = self.command

        env: Union[Unset, dict[str, Any]] = UNSET
        if self.env and not isinstance(self.env, Unset) and not isinstance(self.env, dict):
            env = self.env.to_dict()
        elif self.env and isinstance(self.env, dict):
            env = self.env

        keep_alive = self.keep_alive

        name = self.name

        timeout = self.timeout

        working_dir = self.working_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["command"] = command
        if env is not UNSET:
            field_dict["env"] = env
        if keep_alive is not UNSET:
            field_dict["keepAlive"] = keep_alive
        if name is not UNSET:
            field_dict["name"] = name
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if working_dir is not UNSET:
            field_dict["workingDir"] = working_dir

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_schedule_input_env import SandboxScheduleInputEnv

        if not src_dict:
            return None
        d = src_dict.copy()
        command = d.pop("command", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, SandboxScheduleInputEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = SandboxScheduleInputEnv.from_dict(_env)

        keep_alive = d.pop("keepAlive", d.pop("keep_alive", UNSET))

        name = d.pop("name", UNSET)

        timeout = d.pop("timeout", UNSET)

        working_dir = d.pop("workingDir", d.pop("working_dir", UNSET))

        sandbox_schedule_input = cls(
            command=command,
            env=env,
            keep_alive=keep_alive,
            name=name,
            timeout=timeout,
            working_dir=working_dir,
        )

        sandbox_schedule_input.additional_properties = d
        return sandbox_schedule_input

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
