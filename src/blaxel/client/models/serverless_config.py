from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerlessConfig")


@_attrs_define
class ServerlessConfig:
    """Configuration for a serverless deployment

    Attributes:
        max_scale (Union[Unset, int]): The minimum number of replicas for the deployment. Can be 0 or 1 (in which case
            the deployment is always running in at least one location).
        min_scale (Union[Unset, int]): The maximum number of replicas for the deployment.
        timeout (Union[Unset, int]): The timeout for the deployment in seconds
    """

    max_scale: Union[Unset, int] = UNSET
    min_scale: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_scale = self.max_scale

        min_scale = self.min_scale

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_scale is not UNSET:
            field_dict["maxScale"] = max_scale
        if min_scale is not UNSET:
            field_dict["minScale"] = min_scale
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        max_scale = d.pop("maxScale", UNSET)

        min_scale = d.pop("minScale", UNSET)

        timeout = d.pop("timeout", UNSET)

        serverless_config = cls(
            max_scale=max_scale,
            min_scale=min_scale,
            timeout=timeout,
        )

        serverless_config.additional_properties = d
        return serverless_config

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
