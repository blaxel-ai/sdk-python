from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_endpoint_token import IntegrationEndpointToken


T = TypeVar("T", bound="IntegrationEndpoint")


@_attrs_define
class IntegrationEndpoint:
    """Integration endpoint

    Attributes:
        body (Union[Unset, str]): Integration endpoint body
        ignore_models (Union[Unset, list[Any]]): Integration endpoint ignore models
        method (Union[Unset, str]): Integration endpoint method
        models (Union[Unset, list[Any]]): Integration endpoint models
        stream_key (Union[Unset, str]): Integration endpoint stream key
        stream_token (Union[Unset, IntegrationEndpointToken]): Integration endpoint token
        token (Union[Unset, IntegrationEndpointToken]): Integration endpoint token
    """

    body: Union[Unset, str] = UNSET
    ignore_models: Union[Unset, list[Any]] = UNSET
    method: Union[Unset, str] = UNSET
    models: Union[Unset, list[Any]] = UNSET
    stream_key: Union[Unset, str] = UNSET
    stream_token: Union[Unset, "IntegrationEndpointToken"] = UNSET
    token: Union[Unset, "IntegrationEndpointToken"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        ignore_models: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.ignore_models, Unset):
            ignore_models = self.ignore_models

        method = self.method

        models: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.models, Unset):
            models = self.models

        stream_key = self.stream_key

        stream_token: Union[Unset, dict[str, Any]] = UNSET
        if self.stream_token and not isinstance(self.stream_token, Unset) and not isinstance(self.stream_token, dict):
            stream_token = self.stream_token.to_dict()
        elif self.stream_token and isinstance(self.stream_token, dict):
            stream_token = self.stream_token

        token: Union[Unset, dict[str, Any]] = UNSET
        if self.token and not isinstance(self.token, Unset) and not isinstance(self.token, dict):
            token = self.token.to_dict()
        elif self.token and isinstance(self.token, dict):
            token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if ignore_models is not UNSET:
            field_dict["ignoreModels"] = ignore_models
        if method is not UNSET:
            field_dict["method"] = method
        if models is not UNSET:
            field_dict["models"] = models
        if stream_key is not UNSET:
            field_dict["streamKey"] = stream_key
        if stream_token is not UNSET:
            field_dict["streamToken"] = stream_token
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.integration_endpoint_token import IntegrationEndpointToken

        if not src_dict:
            return None
        d = src_dict.copy()
        body = d.pop("body", UNSET)

        ignore_models = cast(list[Any], d.pop("ignoreModels", UNSET))

        method = d.pop("method", UNSET)

        models = cast(list[Any], d.pop("models", UNSET))

        stream_key = d.pop("streamKey", UNSET)

        _stream_token = d.pop("streamToken", UNSET)
        stream_token: Union[Unset, IntegrationEndpointToken]
        if isinstance(_stream_token, Unset):
            stream_token = UNSET
        else:
            stream_token = IntegrationEndpointToken.from_dict(_stream_token)

        _token = d.pop("token", UNSET)
        token: Union[Unset, IntegrationEndpointToken]
        if isinstance(_token, Unset):
            token = UNSET
        else:
            token = IntegrationEndpointToken.from_dict(_token)

        integration_endpoint = cls(
            body=body,
            ignore_models=ignore_models,
            method=method,
            models=models,
            stream_key=stream_key,
            stream_token=stream_token,
            token=token,
        )

        integration_endpoint.additional_properties = d
        return integration_endpoint

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
