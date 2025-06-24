from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        port (Union[Unset, int]): Port of the preview
        prefix_url (Union[Unset, str]): Prefix URL
        public (Union[Unset, bool]): Whether the preview is public
        request_headers (Union[Unset, PreviewSpecRequestHeaders]): Those headers will be set in all requests to your
            preview. This is especially useful to set the Authorization header.
        response_headers (Union[Unset, PreviewSpecResponseHeaders]): Those headers will be set in all responses of your
            preview. This is especially useful to set the CORS headers.
        url (Union[Unset, str]): URL of the preview
    """

    port: Union[Unset, int] = UNSET
    prefix_url: Union[Unset, str] = UNSET
    public: Union[Unset, bool] = UNSET
    request_headers: Union[Unset, "PreviewSpecRequestHeaders"] = UNSET
    response_headers: Union[Unset, "PreviewSpecResponseHeaders"] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        port = self.port

        prefix_url = self.prefix_url

        public = self.public

        request_headers: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_headers
            and not isinstance(self.request_headers, Unset)
            and not isinstance(self.request_headers, dict)
        ):
            request_headers = self.request_headers.to_dict()
        elif self.request_headers and isinstance(self.request_headers, dict):
            request_headers = self.request_headers

        response_headers: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.response_headers
            and not isinstance(self.response_headers, Unset)
            and not isinstance(self.response_headers, dict)
        ):
            response_headers = self.response_headers.to_dict()
        elif self.response_headers and isinstance(self.response_headers, dict):
            response_headers = self.response_headers

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if port is not UNSET:
            field_dict["port"] = port
        if prefix_url is not UNSET:
            field_dict["prefixUrl"] = prefix_url
        if public is not UNSET:
            field_dict["public"] = public
        if request_headers is not UNSET:
            field_dict["requestHeaders"] = request_headers
        if response_headers is not UNSET:
            field_dict["responseHeaders"] = response_headers
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.preview_spec_request_headers import PreviewSpecRequestHeaders
        from ..models.preview_spec_response_headers import PreviewSpecResponseHeaders

        if not src_dict:
            return None
        d = src_dict.copy()
        port = d.pop("port", UNSET)

        prefix_url = d.pop("prefixUrl", UNSET)

        public = d.pop("public", UNSET)

        _request_headers = d.pop("requestHeaders", UNSET)
        request_headers: Union[Unset, PreviewSpecRequestHeaders]
        if isinstance(_request_headers, Unset):
            request_headers = UNSET
        else:
            request_headers = PreviewSpecRequestHeaders.from_dict(_request_headers)

        _response_headers = d.pop("responseHeaders", UNSET)
        response_headers: Union[Unset, PreviewSpecResponseHeaders]
        if isinstance(_response_headers, Unset):
            response_headers = UNSET
        else:
            response_headers = PreviewSpecResponseHeaders.from_dict(_response_headers)

        url = d.pop("url", UNSET)

        preview_spec = cls(
            port=port,
            prefix_url=prefix_url,
            public=public,
            request_headers=request_headers,
            response_headers=response_headers,
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
