from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShareImageBody")


@_attrs_define
class ShareImageBody:
    """
    Attributes:
        target_workspace (str): Name of the workspace to share the image with
        target_account_id (Union[Unset, str]): Account ID of the target workspace. Required when the target workspace
            belongs to a different account than the source workspace (anti-spam).
    """

    target_workspace: str
    target_account_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_workspace = self.target_workspace

        target_account_id = self.target_account_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "targetWorkspace": target_workspace,
            }
        )
        if target_account_id is not UNSET:
            field_dict["targetAccountId"] = target_account_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        target_workspace = (
            d.pop("targetWorkspace") if "targetWorkspace" in d else d.pop("target_workspace")
        )

        target_account_id = d.pop("targetAccountId", d.pop("target_account_id", UNSET))

        share_image_body = cls(
            target_workspace=target_workspace,
            target_account_id=target_account_id,
        )

        share_image_body.additional_properties = d
        return share_image_body

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
