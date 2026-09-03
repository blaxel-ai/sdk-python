from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MultipartUpload")


@_attrs_define
class MultipartUpload:
    """
    Attributes:
        abort_url (Union[Unset, str]): AbortURL is a presigned DELETE URL that discards the parts already
            uploaded. Without it a failed export leaves them on the storage until a
            lifecycle rule removes them.
        complete_url (Union[Unset, str]): CompleteURL is a presigned POST URL that assembles the parts.
        part_size (Union[Unset, int]): PartSize is the number of bytes sent to every part but the last. Example:
            536870912.
        part_urls (Union[Unset, list[str]]): PartURLs are presigned PUT URLs, one per part, in order. Extra ones are
            left unused.
    """

    abort_url: Union[Unset, str] = UNSET
    complete_url: Union[Unset, str] = UNSET
    part_size: Union[Unset, int] = UNSET
    part_urls: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        abort_url = self.abort_url

        complete_url = self.complete_url

        part_size = self.part_size

        part_urls: Union[Unset, list[str]] = UNSET
        if not isinstance(self.part_urls, Unset):
            part_urls = self.part_urls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abort_url is not UNSET:
            field_dict["abortUrl"] = abort_url
        if complete_url is not UNSET:
            field_dict["completeUrl"] = complete_url
        if part_size is not UNSET:
            field_dict["partSize"] = part_size
        if part_urls is not UNSET:
            field_dict["partUrls"] = part_urls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        abort_url = d.pop("abortUrl", d.pop("abort_url", UNSET))

        complete_url = d.pop("completeUrl", d.pop("complete_url", UNSET))

        part_size = d.pop("partSize", d.pop("part_size", UNSET))

        part_urls = cast(list[str], d.pop("partUrls", d.pop("part_urls", UNSET)))

        multipart_upload = cls(
            abort_url=abort_url,
            complete_url=complete_url,
            part_size=part_size,
            part_urls=part_urls,
        )

        multipart_upload.additional_properties = d
        return multipart_upload

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
