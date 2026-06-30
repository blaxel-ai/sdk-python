from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_schedule_entry_type import SandboxScheduleEntryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_schedule_input import SandboxScheduleInput


T = TypeVar("T", bound="SandboxScheduleEntry")


@_attrs_define
class SandboxScheduleEntry:
    """A scheduled task that executes a process inside the sandbox at specified times. Stored in the dedicated schedules
    table (no longer embedded in the sandbox spec).

        Attributes:
            created_at (Union[Unset, str]): Creation timestamp (read-only).
            id (Union[Unset, str]): Unique identifier for this schedule within its sandbox. Auto-generated if not provided.
                Example: schedule-0.
            input_ (Union[Unset, SandboxScheduleInput]): Process execution configuration for a scheduled sandbox task
            max_executions (Union[Unset, int]): Maximum number of execution records kept for this schedule. Once reached,
                recording a new execution deletes the oldest. Defaults to 100. Example: 100.
            type_ (Union[Unset, SandboxScheduleEntryType]): Type of schedule timing. 'cron' for recurring (5-field
                expression), 'at' for a specific RFC 3339 datetime, 'sleep' for a duration from now (resolved to 'at' on
                creation). Example: cron.
            value (Union[Unset, str]): Timing value. For 'cron': a 5-field cron expression (e.g. '0 8 * * 1-5'). For 'at':
                an RFC 3339 datetime (e.g. '2026-07-01T09:00:00Z'). For 'sleep': a duration (e.g. '2h', '30m', '7d'). Example: 0
                8 * * 1-5.
    """

    created_at: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    input_: Union[Unset, "SandboxScheduleInput"] = UNSET
    max_executions: Union[Unset, int] = UNSET
    type_: Union[Unset, SandboxScheduleEntryType] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        created_at = self.created_at

        id = self.id

        input_: Union[Unset, dict[str, Any]] = UNSET
        if self.input_ and not isinstance(self.input_, Unset) and not isinstance(self.input_, dict):
            input_ = self.input_.to_dict()
        elif self.input_ and isinstance(self.input_, dict):
            input_ = self.input_

        max_executions = self.max_executions

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if max_executions is not UNSET:
            field_dict["maxExecutions"] = max_executions
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_schedule_input import SandboxScheduleInput

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        id = d.pop("id", UNSET)

        _input_ = d.pop("input", d.pop("input_", UNSET))
        input_: Union[Unset, SandboxScheduleInput]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = SandboxScheduleInput.from_dict(_input_)

        max_executions = d.pop("maxExecutions", d.pop("max_executions", UNSET))

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: Union[Unset, SandboxScheduleEntryType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SandboxScheduleEntryType(_type_)

        value = d.pop("value", UNSET)

        sandbox_schedule_entry = cls(
            created_at=created_at,
            id=id,
            input_=input_,
            max_executions=max_executions,
            type_=type_,
            value=value,
        )

        sandbox_schedule_entry.additional_properties = d
        return sandbox_schedule_entry

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
