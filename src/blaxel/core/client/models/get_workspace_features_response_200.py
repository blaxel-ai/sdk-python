from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_workspace_features_response_200_features import (
        GetWorkspaceFeaturesResponse200Features,
    )


T = TypeVar("T", bound="GetWorkspaceFeaturesResponse200")


@_attrs_define
class GetWorkspaceFeaturesResponse200:
    """
    Attributes:
        features (Union[Unset, GetWorkspaceFeaturesResponse200Features]): Map of feature keys to enabled state (always
            true). Disabled features are omitted.
    """

    features: Union[Unset, "GetWorkspaceFeaturesResponse200Features"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        features: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.features
            and not isinstance(self.features, Unset)
            and not isinstance(self.features, dict)
        ):
            features = self.features.to_dict()
        elif self.features and isinstance(self.features, dict):
            features = self.features

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if features is not UNSET:
            field_dict["features"] = features

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.get_workspace_features_response_200_features import (
            GetWorkspaceFeaturesResponse200Features,
        )

        if not src_dict:
            return None
        d = src_dict.copy()
        _features = d.pop("features", UNSET)
        features: Union[Unset, GetWorkspaceFeaturesResponse200Features]
        if isinstance(_features, Unset):
            features = UNSET
        else:
            features = GetWorkspaceFeaturesResponse200Features.from_dict(_features)

        get_workspace_features_response_200 = cls(
            features=features,
        )

        get_workspace_features_response_200.additional_properties = d
        return get_workspace_features_response_200

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
