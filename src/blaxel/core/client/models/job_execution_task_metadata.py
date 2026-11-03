from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionTaskMetadata")


@_attrs_define
class JobExecutionTaskMetadata:
    """Job execution task metadata

    Attributes:
        completed_at (str | Unset): Completion timestamp
        created_at (str | Unset): Creation timestamp
        name (str | Unset): Task name Example: task-0.
        scheduled_at (str | Unset): Scheduled timestamp
        started_at (str | Unset): Start timestamp
        updated_at (str | Unset): Last update timestamp
    """

    completed_at: str | Unset = UNSET
    created_at: str | Unset = UNSET
    name: str | Unset = UNSET
    scheduled_at: str | Unset = UNSET
    started_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed_at = self.completed_at

        created_at = self.created_at

        name = self.name

        scheduled_at = self.scheduled_at

        started_at = self.started_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if name is not UNSET:
            field_dict["name"] = name
        if scheduled_at is not UNSET:
            field_dict["scheduledAt"] = scheduled_at
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        completed_at = d.pop("completedAt", d.pop("completed_at", UNSET))

        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        name = d.pop("name", UNSET)

        scheduled_at = d.pop("scheduledAt", d.pop("scheduled_at", UNSET))

        started_at = d.pop("startedAt", d.pop("started_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        job_execution_task_metadata = cls(
            completed_at=completed_at,
            created_at=created_at,
            name=name,
            scheduled_at=scheduled_at,
            started_at=started_at,
            updated_at=updated_at,
        )

        job_execution_task_metadata.additional_properties = d
        return job_execution_task_metadata

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
