from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.template_variable import TemplateVariable


T = TypeVar("T", bound="Template")


@_attrs_define
class Template:
    """Blaxel template

    Attributes:
        default_branch (str | Unset): Default branch of the template Example: main.
        description (str | Unset): Description of the template Example: A starter template for building LangChain
            agents.
        download_count (int | Unset): Number of downloads/clones of the repository Example: 1200.
        forks_count (int | Unset): Number of forks the repository has Example: 45.
        icon (str | Unset): URL to the template's icon
        icon_dark (str | Unset): URL to the template's icon in dark mode
        name (str | Unset): Name of the template Example: langchain-agent.
        sha (str | Unset): SHA of the variable
        star_count (int | Unset): Number of stars the repository has Example: 150.
        topics (list[str] | Unset): Topic of the template
        url (str | Unset): URL of the template Example: https://github.com/blaxel-ai/template-langchain-agent.
        variables (list[TemplateVariable] | Unset): Variables of the template
    """

    default_branch: str | Unset = UNSET
    description: str | Unset = UNSET
    download_count: int | Unset = UNSET
    forks_count: int | Unset = UNSET
    icon: str | Unset = UNSET
    icon_dark: str | Unset = UNSET
    name: str | Unset = UNSET
    sha: str | Unset = UNSET
    star_count: int | Unset = UNSET
    topics: list[str] | Unset = UNSET
    url: str | Unset = UNSET
    variables: list[TemplateVariable] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_branch = self.default_branch

        description = self.description

        download_count = self.download_count

        forks_count = self.forks_count

        icon = self.icon

        icon_dark = self.icon_dark

        name = self.name

        sha = self.sha

        star_count = self.star_count

        topics: list[str] | Unset = UNSET
        if not isinstance(self.topics, Unset):
            topics = self.topics

        url = self.url

        variables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                if type(variables_item_data) is dict:
                    variables_item = variables_item_data
                else:
                    variables_item = variables_item_data.to_dict()
                variables.append(variables_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_branch is not UNSET:
            field_dict["defaultBranch"] = default_branch
        if description is not UNSET:
            field_dict["description"] = description
        if download_count is not UNSET:
            field_dict["downloadCount"] = download_count
        if forks_count is not UNSET:
            field_dict["forksCount"] = forks_count
        if icon is not UNSET:
            field_dict["icon"] = icon
        if icon_dark is not UNSET:
            field_dict["iconDark"] = icon_dark
        if name is not UNSET:
            field_dict["name"] = name
        if sha is not UNSET:
            field_dict["sha"] = sha
        if star_count is not UNSET:
            field_dict["starCount"] = star_count
        if topics is not UNSET:
            field_dict["topics"] = topics
        if url is not UNSET:
            field_dict["url"] = url
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.template_variable import TemplateVariable  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        default_branch = d.pop("defaultBranch", d.pop("default_branch", UNSET))

        description = d.pop("description", UNSET)

        download_count = d.pop("downloadCount", d.pop("download_count", UNSET))

        forks_count = d.pop("forksCount", d.pop("forks_count", UNSET))

        icon = d.pop("icon", UNSET)

        icon_dark = d.pop("iconDark", d.pop("icon_dark", UNSET))

        name = d.pop("name", UNSET)

        sha = d.pop("sha", UNSET)

        star_count = d.pop("starCount", d.pop("star_count", UNSET))

        topics = cast(list[str], d.pop("topics", UNSET))

        url = d.pop("url", UNSET)

        variables = []
        _variables = d.pop("variables", UNSET)
        for variables_item_data in _variables or []:
            variables_item = TemplateVariable.from_dict(variables_item_data)

            variables.append(variables_item)

        template = cls(
            default_branch=default_branch,
            description=description,
            download_count=download_count,
            forks_count=forks_count,
            icon=icon,
            icon_dark=icon_dark,
            name=name,
            sha=sha,
            star_count=star_count,
            topics=topics,
            url=url,
            variables=variables,
        )

        template.additional_properties = d
        return template

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
