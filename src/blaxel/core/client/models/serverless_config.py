from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.serverless_config_configuration import ServerlessConfigConfiguration


T = TypeVar("T", bound="ServerlessConfig")


@_attrs_define
class ServerlessConfig:
    """Configuration for a serverless deployment

    Attributes:
        configuration (Union[Unset, ServerlessConfigConfiguration]): The configuration for the deployment
        max_retries (Union[Unset, int]): The maximum number of retries for the deployment
        max_scale (Union[Unset, int]): The minimum number of replicas for the deployment. Can be 0 or 1 (in which case
            the deployment is always running in at least one location).
        min_scale (Union[Unset, int]): The maximum number of replicas for the deployment.
        timeout (Union[Unset, int]): The timeout for the deployment in seconds
    """

    configuration: Union[Unset, "ServerlessConfigConfiguration"] = UNSET
    max_retries: Union[Unset, int] = UNSET
    max_scale: Union[Unset, int] = UNSET
    min_scale: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configuration: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.configuration
            and not isinstance(self.configuration, Unset)
            and not isinstance(self.configuration, dict)
        ):
            configuration = self.configuration.to_dict()
        elif self.configuration and isinstance(self.configuration, dict):
            configuration = self.configuration

        max_retries = self.max_retries

        max_scale = self.max_scale

        min_scale = self.min_scale

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if max_retries is not UNSET:
            field_dict["maxRetries"] = max_retries
        if max_scale is not UNSET:
            field_dict["maxScale"] = max_scale
        if min_scale is not UNSET:
            field_dict["minScale"] = min_scale
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.serverless_config_configuration import ServerlessConfigConfiguration

        if not src_dict:
            return None
        d = src_dict.copy()
        _configuration = d.pop("configuration", UNSET)
        configuration: Union[Unset, ServerlessConfigConfiguration]
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = ServerlessConfigConfiguration.from_dict(_configuration)

        max_retries = d.pop("maxRetries", UNSET)

        max_scale = d.pop("maxScale", UNSET)

        min_scale = d.pop("minScale", UNSET)

        timeout = d.pop("timeout", UNSET)

        serverless_config = cls(
            configuration=configuration,
            max_retries=max_retries,
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
