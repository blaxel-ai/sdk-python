from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.preview_spec_request_headers import PreviewSpecRequestHeaders
    from ..models.preview_spec_response_headers import PreviewSpecResponseHeaders


T = TypeVar("T", bound="PreviewSpec")


@_attrs_define
class PreviewSpec:
    """Preview of a Resource

    Attributes:
        custom_domain (str | Unset): Custom domain bound to this preview
        expires (str | Unset): The expiration date for the preview in ISO 8601 format - 2024-12-31T23:59:59Z
        port (int | Unset): Port of the preview
        prefix_url (str | Unset): Prefix URL
        public (bool | Unset): Whether the preview is public
        region (str | Unset): Region where the preview is deployed, this is readonly
        request_headers (PreviewSpecRequestHeaders | Unset): Those headers will be set in all requests to your preview.
            This is especially useful to set the Authorization header.
        response_headers (PreviewSpecResponseHeaders | Unset): Those headers will be set in all responses of your
            preview. This is especially useful to set the CORS headers.
        ttl (str | Unset): Time to live for the preview (e.g., "1h", "24h", "7d"). After this duration, the preview will
            be automatically deleted.
        url (str | Unset): URL of the preview
    """

    custom_domain: str | Unset = UNSET
    expires: str | Unset = UNSET
    port: int | Unset = UNSET
    prefix_url: str | Unset = UNSET
    public: bool | Unset = UNSET
    region: str | Unset = UNSET
    request_headers: PreviewSpecRequestHeaders | Unset = UNSET
    response_headers: PreviewSpecResponseHeaders | Unset = UNSET
    ttl: str | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        custom_domain = self.custom_domain

        expires = self.expires

        port = self.port

        prefix_url = self.prefix_url

        public = self.public

        region = self.region

        request_headers: dict[str, Any] | Unset = UNSET
        if (
            self.request_headers
            and not isinstance(self.request_headers, Unset)
            and not isinstance(self.request_headers, dict)
        ):
            request_headers = self.request_headers.to_dict()
        elif self.request_headers and isinstance(self.request_headers, dict):
            request_headers = self.request_headers

        response_headers: dict[str, Any] | Unset = UNSET
        if (
            self.response_headers
            and not isinstance(self.response_headers, Unset)
            and not isinstance(self.response_headers, dict)
        ):
            response_headers = self.response_headers.to_dict()
        elif self.response_headers and isinstance(self.response_headers, dict):
            response_headers = self.response_headers

        ttl = self.ttl

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if custom_domain is not UNSET:
            field_dict["customDomain"] = custom_domain
        if expires is not UNSET:
            field_dict["expires"] = expires
        if port is not UNSET:
            field_dict["port"] = port
        if prefix_url is not UNSET:
            field_dict["prefixUrl"] = prefix_url
        if public is not UNSET:
            field_dict["public"] = public
        if region is not UNSET:
            field_dict["region"] = region
        if request_headers is not UNSET:
            field_dict["requestHeaders"] = request_headers
        if response_headers is not UNSET:
            field_dict["responseHeaders"] = response_headers
        if ttl is not UNSET:
            field_dict["ttl"] = ttl
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.preview_spec_request_headers import PreviewSpecRequestHeaders  # noqa: PLC0415
        from ..models.preview_spec_response_headers import (
            PreviewSpecResponseHeaders,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        custom_domain = d.pop("customDomain", d.pop("custom_domain", UNSET))

        expires = d.pop("expires", UNSET)

        port = d.pop("port", UNSET)

        prefix_url = d.pop("prefixUrl", d.pop("prefix_url", UNSET))

        public = d.pop("public", UNSET)

        region = d.pop("region", UNSET)

        _request_headers = d.pop("requestHeaders", d.pop("request_headers", UNSET))
        request_headers: PreviewSpecRequestHeaders | Unset
        if isinstance(_request_headers, Unset):
            request_headers = UNSET
        else:
            request_headers = PreviewSpecRequestHeaders.from_dict(_request_headers)

        _response_headers = d.pop("responseHeaders", d.pop("response_headers", UNSET))
        response_headers: PreviewSpecResponseHeaders | Unset
        if isinstance(_response_headers, Unset):
            response_headers = UNSET
        else:
            response_headers = PreviewSpecResponseHeaders.from_dict(_response_headers)

        ttl = d.pop("ttl", UNSET)

        url = d.pop("url", UNSET)

        preview_spec = cls(
            custom_domain=custom_domain,
            expires=expires,
            port=port,
            prefix_url=prefix_url,
            public=public,
            region=region,
            request_headers=request_headers,
            response_headers=response_headers,
            ttl=ttl,
            url=url,
        )

        preview_spec.additional_properties = d
        return preview_spec

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
