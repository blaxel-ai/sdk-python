from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entrypoint_env import EntrypointEnv


T = TypeVar("T", bound="Entrypoint")


@_attrs_define
class Entrypoint:
    """Entrypoint of the artifact

    Attributes:
        args (Union[Unset, list[Any]]): Args of the entrypoint
        command (Union[Unset, str]): Command of the entrypoint
        env (Union[Unset, EntrypointEnv]): Env of the entrypoint
    """

    args: Union[Unset, list[Any]] = UNSET
    command: Union[Unset, str] = UNSET
    env: Union[Unset, "EntrypointEnv"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        args: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        command = self.command

        env: Union[Unset, dict[str, Any]] = UNSET
        if self.env and not isinstance(self.env, Unset) and not isinstance(self.env, dict):
            env = self.env.to_dict()
        elif self.env and isinstance(self.env, dict):
            env = self.env

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args
        if command is not UNSET:
            field_dict["command"] = command
        if env is not UNSET:
            field_dict["env"] = env

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entrypoint_env import EntrypointEnv

        if not src_dict:
            return None
        d = src_dict.copy()
        args = cast(list[Any], d.pop("args", UNSET))

        command = d.pop("command", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, EntrypointEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = EntrypointEnv.from_dict(_env)

        entrypoint = cls(
            args=args,
            command=command,
            env=env,
        )

        entrypoint.additional_properties = d
        return entrypoint

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
