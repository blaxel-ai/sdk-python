from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        default_branch (Union[Unset, str]): Default branch of the template
        description (Union[Unset, str]): Description of the template
        download_count (Union[Unset, int]): Number of downloads/clones of the repository
        forks_count (Union[Unset, int]): Number of forks the repository has
        icon (Union[Unset, str]): URL to the template's icon
        icon_dark (Union[Unset, str]): URL to the template's icon in dark mode
        name (Union[Unset, str]): Name of the template
        sha (Union[Unset, str]): SHA of the variable
        star_count (Union[Unset, int]): Number of stars the repository has
        topics (Union[Unset, list[str]]): Topic of the template
        url (Union[Unset, str]): URL of the template
        variables (Union[Unset, list['TemplateVariable']]): Variables of the template
    """

    default_branch: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    download_count: Union[Unset, int] = UNSET
    forks_count: Union[Unset, int] = UNSET
    icon: Union[Unset, str] = UNSET
    icon_dark: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    sha: Union[Unset, str] = UNSET
    star_count: Union[Unset, int] = UNSET
    topics: Union[Unset, list[str]] = UNSET
    url: Union[Unset, str] = UNSET
    variables: Union[Unset, list["TemplateVariable"]] = UNSET
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

        topics: Union[Unset, list[str]] = UNSET
        if not isinstance(self.topics, Unset):
            topics = self.topics

        url = self.url

        variables: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                if type(variables_item_data) == dict:
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.template_variable import TemplateVariable

        if not src_dict:
            return None
        d = src_dict.copy()
        default_branch = d.pop("defaultBranch", UNSET)

        description = d.pop("description", UNSET)

        download_count = d.pop("downloadCount", UNSET)

        forks_count = d.pop("forksCount", UNSET)

        icon = d.pop("icon", UNSET)

        icon_dark = d.pop("iconDark", UNSET)

        name = d.pop("name", UNSET)

        sha = d.pop("sha", UNSET)

        star_count = d.pop("starCount", UNSET)

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
