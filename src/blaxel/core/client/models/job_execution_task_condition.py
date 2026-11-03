from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionTaskCondition")


@_attrs_define
class JobExecutionTaskCondition:
    """Job execution task condition

    Attributes:
        execution_reason (str | Unset): Execution reason
        message (str | Unset): Condition message
        reason (str | Unset): Condition reason
        severity (str | Unset): Condition severity
        state (str | Unset): Condition state
        type_ (str | Unset): Condition type
    """

    execution_reason: str | Unset = UNSET
    message: str | Unset = UNSET
    reason: str | Unset = UNSET
    severity: str | Unset = UNSET
    state: str | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_reason = self.execution_reason

        message = self.message

        reason = self.reason

        severity = self.severity

        state = self.state

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if execution_reason is not UNSET:
            field_dict["executionReason"] = execution_reason
        if message is not UNSET:
            field_dict["message"] = message
        if reason is not UNSET:
            field_dict["reason"] = reason
        if severity is not UNSET:
            field_dict["severity"] = severity
        if state is not UNSET:
            field_dict["state"] = state
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        execution_reason = d.pop("executionReason", d.pop("execution_reason", UNSET))

        message = d.pop("message", UNSET)

        reason = d.pop("reason", UNSET)

        severity = d.pop("severity", UNSET)

        state = d.pop("state", UNSET)

        type_ = d.pop("type", d.pop("type_", UNSET))

        job_execution_task_condition = cls(
            execution_reason=execution_reason,
            message=message,
            reason=reason,
            severity=severity,
            state=state,
            type_=type_,
        )

        job_execution_task_condition.additional_properties = d
        return job_execution_task_condition

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
