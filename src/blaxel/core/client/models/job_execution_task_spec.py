from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionTaskSpec")


@_attrs_define
class JobExecutionTaskSpec:
    """Job execution task specification

    Attributes:
        max_retries (Union[Unset, int]): Maximum number of retries Example: 3.
        timeout (Union[Unset, str]): Task timeout duration Example: 30m.
    """

    max_retries: Union[Unset, int] = UNSET
    timeout: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_retries = self.max_retries

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_retries is not UNSET:
            field_dict["maxRetries"] = max_retries
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        max_retries = d.pop("maxRetries", d.pop("max_retries", UNSET))

        timeout = d.pop("timeout", UNSET)

        job_execution_task_spec = cls(
            max_retries=max_retries,
            timeout=timeout,
        )

        job_execution_task_spec.additional_properties = d
        return job_execution_task_spec

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
