from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CoreEvent")


@_attrs_define
class CoreEvent:
    """Core event

    Attributes:
        canary_revision (Union[Unset, str]): Canary revisionID link to the event
        message (Union[Unset, str]): Event message Example: Deployment successful.
        revision (Union[Unset, str]): RevisionID link to the event Example: rev-abc123.
        status (Union[Unset, str]): Event status Example: DEPLOYED.
        time (Union[Unset, str]): Event time Example: 2025-01-15T10:30:00Z.
        type_ (Union[Unset, str]): Event type Example: deployment.
    """

    canary_revision: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
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
