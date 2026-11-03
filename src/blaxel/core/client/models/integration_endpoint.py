from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_endpoint_ignore_models_item import IntegrationEndpointIgnoreModelsItem
    from ..models.integration_endpoint_models_item import IntegrationEndpointModelsItem
    from ..models.integration_endpoint_token import IntegrationEndpointToken


T = TypeVar("T", bound="IntegrationEndpoint")


@_attrs_define
class IntegrationEndpoint:
    """Integration endpoint

    Attributes:
        body (str | Unset): Integration endpoint body
        ignore_models (list[IntegrationEndpointIgnoreModelsItem] | Unset): Integration endpoint ignore models
        method (str | Unset): Integration endpoint method
        models (list[IntegrationEndpointModelsItem] | Unset): Integration endpoint models
        stream_key (str | Unset): Integration endpoint stream key
        stream_token (IntegrationEndpointToken | Unset): Integration endpoint token
        token (IntegrationEndpointToken | Unset): Integration endpoint token
    """

    body: str | Unset = UNSET
    ignore_models: list[IntegrationEndpointIgnoreModelsItem] | Unset = UNSET
    method: str | Unset = UNSET
    models: list[IntegrationEndpointModelsItem] | Unset = UNSET
    stream_key: str | Unset = UNSET
    stream_token: IntegrationEndpointToken | Unset = UNSET
    token: IntegrationEndpointToken | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        ignore_models: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ignore_models, Unset):
            ignore_models = []
            for ignore_models_item_data in self.ignore_models:
                if type(ignore_models_item_data) is dict:
                    ignore_models_item = ignore_models_item_data
                else:
                    ignore_models_item = ignore_models_item_data.to_dict()
                ignore_models.append(ignore_models_item)

        method = self.method

        models: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                if type(models_item_data) is dict:
                    models_item = models_item_data
                else:
                    models_item = models_item_data.to_dict()
                models.append(models_item)

        stream_key = self.stream_key

        stream_token: dict[str, Any] | Unset = UNSET
        if (
            self.stream_token
            and not isinstance(self.stream_token, Unset)
            and not isinstance(self.stream_token, dict)
        ):
            stream_token = self.stream_token.to_dict()
        elif self.stream_token and isinstance(self.stream_token, dict):
            stream_token = self.stream_token

        token: dict[str, Any] | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.integration_endpoint_ignore_models_item import (
            IntegrationEndpointIgnoreModelsItem,
        )  # noqa: PLC0415
        from ..models.integration_endpoint_models_item import (
            IntegrationEndpointModelsItem,  # noqa: PLC0415
        )
        from ..models.integration_endpoint_token import IntegrationEndpointToken  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        body = d.pop("body", UNSET)

        ignore_models = []
        _ignore_models = d.pop("ignoreModels", d.pop("ignore_models", UNSET))
        for ignore_models_item_data in _ignore_models or []:
            ignore_models_item = IntegrationEndpointIgnoreModelsItem.from_dict(
                ignore_models_item_data
            )

            ignore_models.append(ignore_models_item)

        method = d.pop("method", UNSET)

        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in _models or []:
            models_item = IntegrationEndpointModelsItem.from_dict(models_item_data)

            models.append(models_item)

        stream_key = d.pop("streamKey", d.pop("stream_key", UNSET))

        _stream_token = d.pop("streamToken", d.pop("stream_token", UNSET))
        stream_token: IntegrationEndpointToken | Unset
        if isinstance(_stream_token, Unset):
            stream_token = UNSET
        else:
            stream_token = IntegrationEndpointToken.from_dict(_stream_token)

        _token = d.pop("token", UNSET)
        token: IntegrationEndpointToken | Unset
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
