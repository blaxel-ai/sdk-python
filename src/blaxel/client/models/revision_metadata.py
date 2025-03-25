from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RevisionMetadata")


@_attrs_define
class RevisionMetadata:
    """Revision metadata

    Attributes:
        active (Union[Unset, bool]): Is the revision active
        canary (Union[Unset, bool]): Is the revision canary
        created_at (Union[Unset, str]): Revision created at
        created_by (Union[Unset, str]): Revision created by
        id (Union[Unset, str]): Revision ID
        previous_active (Union[Unset, bool]): Is the revision previous active
        status (Union[Unset, str]): Status of the revision
        traffic_percent (Union[Unset, int]): Percent of traffic to the revision
    """

    active: Union[Unset, bool] = UNSET
    canary: Union[Unset, bool] = UNSET
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    previous_active: Union[Unset, bool] = UNSET
    status: Union[Unset, str] = UNSET
    traffic_percent: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active = self.active

        canary = self.canary

        created_at = self.created_at

        created_by = self.created_by

        id = self.id

        previous_active = self.previous_active

        status = self.status

        traffic_percent = self.traffic_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if canary is not UNSET:
            field_dict["canary"] = canary
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if id is not UNSET:
            field_dict["id"] = id
        if previous_active is not UNSET:
            field_dict["previousActive"] = previous_active
        if status is not UNSET:
            field_dict["status"] = status
        if traffic_percent is not UNSET:
            field_dict["trafficPercent"] = traffic_percent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        active = d.pop("active", UNSET)

        canary = d.pop("canary", UNSET)

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        id = d.pop("id", UNSET)

        previous_active = d.pop("previousActive", UNSET)

        status = d.pop("status", UNSET)

        traffic_percent = d.pop("trafficPercent", UNSET)

        revision_metadata = cls(
            active=active,
            canary=canary,
            created_at=created_at,
            created_by=created_by,
            id=id,
            previous_active=previous_active,
            status=status,
            traffic_percent=traffic_percent,
        )

        revision_metadata.additional_properties = d
        return revision_metadata

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
