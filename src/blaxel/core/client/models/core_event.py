from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CoreEvent")


@_attrs_define
class CoreEvent:
    """Core event

    Attributes:
        canary_revision (str | Unset): Canary revisionID link to the event
        message (str | Unset): Event message Example: Deployment successful.
        revision (str | Unset): RevisionID link to the event Example: rev-abc123.
        status (str | Unset): Event status Example: DEPLOYED.
        time (str | Unset): Event time Example: 2025-01-15T10:30:00Z.
        type_ (str | Unset): Event type Example: deployment.
    """

    canary_revision: str | Unset = UNSET
    message: str | Unset = UNSET
    revision: str | Unset = UNSET
    status: str | Unset = UNSET
    time: str | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        canary_revision = self.canary_revision

        message = self.message

        revision = self.revision

        status = self.status

        time = self.time

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if canary_revision is not UNSET:
            field_dict["canaryRevision"] = canary_revision
        if message is not UNSET:
            field_dict["message"] = message
        if revision is not UNSET:
            field_dict["revision"] = revision
        if status is not UNSET:
            field_dict["status"] = status
        if time is not UNSET:
            field_dict["time"] = time
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        canary_revision = d.pop("canaryRevision", d.pop("canary_revision", UNSET))

        message = d.pop("message", UNSET)

        revision = d.pop("revision", UNSET)

        status = d.pop("status", UNSET)

        time = d.pop("time", UNSET)

        type_ = d.pop("type", d.pop("type_", UNSET))

        core_event = cls(
            canary_revision=canary_revision,
            message=message,
            revision=revision,
            status=status,
            time=time,
            type_=type_,
        )

        core_event.additional_properties = d
        return core_event

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
