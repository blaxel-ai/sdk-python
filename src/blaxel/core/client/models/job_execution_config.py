from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionConfig")


@_attrs_define
class JobExecutionConfig:
    """Configuration for a job execution

    Attributes:
        max_concurrent_tasks (Union[Unset, int]): The maximum number of concurrent tasks for an execution
        max_retries (Union[Unset, int]): The maximum number of retries for the job execution
        timeout (Union[Unset, int]): The timeout for the job execution in seconds
    """

    max_concurrent_tasks: Union[Unset, int] = UNSET
    max_retries: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_concurrent_tasks = self.max_concurrent_tasks

        max_retries = self.max_retries

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_concurrent_tasks is not UNSET:
            field_dict["maxConcurrentTasks"] = max_concurrent_tasks
        if max_retries is not UNSET:
            field_dict["maxRetries"] = max_retries
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        max_concurrent_tasks = d.pop("maxConcurrentTasks", UNSET)

        max_retries = d.pop("maxRetries", UNSET)

        timeout = d.pop("timeout", UNSET)

        job_execution_config = cls(
            max_concurrent_tasks=max_concurrent_tasks,
            max_retries=max_retries,
            timeout=timeout,
        )

        job_execution_config.additional_properties = d
        return job_execution_config

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
