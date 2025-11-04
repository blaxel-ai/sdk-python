from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationModel")


@_attrs_define
class IntegrationModel:
    """Model obtained from an external authentication provider, such as HuggingFace, OpenAI, etc...

    Attributes:
        author (Union[Unset, str]): Provider model author
        created_at (Union[Unset, str]): Provider model created at
        downloads (Union[Unset, int]): Provider model downloads
        endpoint (Union[Unset, str]): Model endpoint URL
        id (Union[Unset, str]): Provider model ID
        library_name (Union[Unset, str]): Provider model library name
        likes (Union[Unset, int]): Provider model likes
        model_private (Union[Unset, str]): Is the model private
        name (Union[Unset, str]): Provider model name
        pipeline_tag (Union[Unset, str]): Provider model pipeline tag
        tags (Union[Unset, list[str]]): Provider model tags
        trending_score (Union[Unset, int]): Provider model trending score
    """

    author: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    downloads: Union[Unset, int] = UNSET
    endpoint: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    library_name: Union[Unset, str] = UNSET
    likes: Union[Unset, int] = UNSET
    model_private: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    pipeline_tag: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    trending_score: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        author = self.author

        created_at = self.created_at

        downloads = self.downloads

        endpoint = self.endpoint

        id = self.id

        library_name = self.library_name

        likes = self.likes

        model_private = self.model_private

        name = self.name

        pipeline_tag = self.pipeline_tag

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        trending_score = self.trending_score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if author is not UNSET:
            field_dict["author"] = author
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if downloads is not UNSET:
            field_dict["downloads"] = downloads
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if id is not UNSET:
            field_dict["id"] = id
        if library_name is not UNSET:
            field_dict["library_name"] = library_name
        if likes is not UNSET:
            field_dict["likes"] = likes
        if model_private is not UNSET:
            field_dict["model_private"] = model_private
        if name is not UNSET:
            field_dict["name"] = name
        if pipeline_tag is not UNSET:
            field_dict["pipeline_tag"] = pipeline_tag
        if tags is not UNSET:
            field_dict["tags"] = tags
        if trending_score is not UNSET:
            field_dict["trending_score"] = trending_score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        author = d.pop("author", UNSET)

        created_at = d.pop("created_at", UNSET)

        downloads = d.pop("downloads", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        id = d.pop("id", UNSET)

        library_name = d.pop("library_name", UNSET)

        likes = d.pop("likes", UNSET)

        model_private = d.pop("model_private", UNSET)

        name = d.pop("name", UNSET)

        pipeline_tag = d.pop("pipeline_tag", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        trending_score = d.pop("trending_score", UNSET)

        integration_model = cls(
            author=author,
            created_at=created_at,
            downloads=downloads,
            endpoint=endpoint,
            id=id,
            library_name=library_name,
            likes=likes,
            model_private=model_private,
            name=name,
            pipeline_tag=pipeline_tag,
            tags=tags,
            trending_score=trending_score,
        )

        integration_model.additional_properties = d
        return integration_model

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
