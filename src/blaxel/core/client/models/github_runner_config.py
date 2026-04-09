from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GithubRunnerConfig")


@_attrs_define
class GithubRunnerConfig:
    """Configuration for running GitHub Actions workflow jobs on Blaxel infrastructure. When repositories are configured,
    the job acts as a self-hosted GitHub Actions runner. Workflow jobs use runs-on with the Blaxel job name to target a
    specific runner.

        Attributes:
            repositories (Union[Unset, list[str]]): Repositories in owner/repo format that this runner is associated with.
                The runner will pick up workflow jobs from any of these repositories. If non-empty, the runner is considered
                enabled. Example: ["my-org/repo-a", "my-org/repo-b"].
    """

    repositories: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        repositories: Union[Unset, list[str]] = UNSET
        if not isinstance(self.repositories, Unset):
            repositories = self.repositories

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if repositories is not UNSET:
            field_dict["repositories"] = repositories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        repositories = cast(list[str], d.pop("repositories", UNSET))

        github_runner_config = cls(
            repositories=repositories,
        )

        github_runner_config.additional_properties = d
        return github_runner_config

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
