from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxInfrastructureError")


@_attrs_define
class SandboxInfrastructureError:
    """Infrastructure failure the compute plane reported for a sandbox

    Attributes:
        code (Union[Unset, str]): Stable code of the failure pattern Example: VM_NETWORK_FAILURE.
        fatal (Union[Unset, bool]): Whether the failure was terminal, putting the sandbox in FAILED, as opposed to being
            cleared by a restart
        instance (Union[Unset, str]): Instance the failure was reported for
        message (Union[Unset, str]): Reason reported with the failure
        time (Union[Unset, str]): Time at which the failure was recorded
    """

    code: Union[Unset, str] = UNSET
    fatal: Union[Unset, bool] = UNSET
    instance: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        fatal = self.fatal

        instance = self.instance

        message = self.message

        time = self.time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if fatal is not UNSET:
            field_dict["fatal"] = fatal
        if instance is not UNSET:
            field_dict["instance"] = instance
        if message is not UNSET:
            field_dict["message"] = message
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        fatal = d.pop("fatal", UNSET)

        instance = d.pop("instance", UNSET)

        message = d.pop("message", UNSET)

        time = d.pop("time", UNSET)

        sandbox_infrastructure_error = cls(
            code=code,
            fatal=fatal,
            instance=instance,
            message=message,
            time=time,
        )

        sandbox_infrastructure_error.additional_properties = d
        return sandbox_infrastructure_error

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
