import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_feature_flag_response_200_payload import TestFeatureFlagResponse200Payload


T = TypeVar("T", bound="TestFeatureFlagResponse200")


@_attrs_define
class TestFeatureFlagResponse200:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        evaluated_at (Union[Unset, datetime.datetime]):
        feature_key (Union[Unset, str]):
        payload (Union[Unset, TestFeatureFlagResponse200Payload]):
        variant (Union[Unset, str]):
    """

    enabled: Union[Unset, bool] = UNSET
    evaluated_at: Union[Unset, datetime.datetime] = UNSET
    feature_key: Union[Unset, str] = UNSET
    payload: Union[Unset, "TestFeatureFlagResponse200Payload"] = UNSET
    variant: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        evaluated_at: Union[Unset, str] = UNSET
        if not isinstance(self.evaluated_at, Unset):
            evaluated_at = self.evaluated_at.isoformat()

        feature_key = self.feature_key

        payload: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.payload
            and not isinstance(self.payload, Unset)
            and not isinstance(self.payload, dict)
        ):
            payload = self.payload.to_dict()
        elif self.payload and isinstance(self.payload, dict):
            payload = self.payload

        variant = self.variant

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if evaluated_at is not UNSET:
            field_dict["evaluatedAt"] = evaluated_at
        if feature_key is not UNSET:
            field_dict["featureKey"] = feature_key
        if payload is not UNSET:
            field_dict["payload"] = payload
        if variant is not UNSET:
            field_dict["variant"] = variant

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.test_feature_flag_response_200_payload import (
            TestFeatureFlagResponse200Payload,
        )

        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        _evaluated_at = d.pop("evaluatedAt", d.pop("evaluated_at", UNSET))
        evaluated_at: Union[Unset, datetime.datetime]
        if isinstance(_evaluated_at, Unset):
            evaluated_at = UNSET
        else:
            evaluated_at = isoparse(_evaluated_at)

        feature_key = d.pop("featureKey", d.pop("feature_key", UNSET))

        _payload = d.pop("payload", UNSET)
        payload: Union[Unset, TestFeatureFlagResponse200Payload]
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = TestFeatureFlagResponse200Payload.from_dict(_payload)

        variant = d.pop("variant", UNSET)

        test_feature_flag_response_200 = cls(
            enabled=enabled,
            evaluated_at=evaluated_at,
            feature_key=feature_key,
            payload=payload,
            variant=variant,
        )

        test_feature_flag_response_200.additional_properties = d
        return test_feature_flag_response_200

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
