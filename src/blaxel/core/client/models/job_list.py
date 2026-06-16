from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job import Job
    from ..models.pagination_meta import PaginationMeta


T = TypeVar("T", bound="JobList")


@_attrs_define
class JobList:
    """Cursor-paginated list of batch jobs. Returned starting with API version 2026-04-28; older API versions return a bare
    array.

        Attributes:
            data (Union[Unset, list['Job']]): Page of jobs.
            meta (Union[Unset, PaginationMeta]): Pagination metadata returned alongside a page of listing results. Always
                present on listing endpoints starting with API version 2026-04-28.
    """

    data: Union[Unset, list["Job"]] = UNSET
    meta: Union[Unset, "PaginationMeta"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                if type(data_item_data) is dict:
                    data_item = data_item_data
                else:
                    data_item = data_item_data.to_dict()
                data.append(data_item)

        meta: Union[Unset, dict[str, Any]] = UNSET
        if self.meta and not isinstance(self.meta, Unset) and not isinstance(self.meta, dict):
            meta = self.meta.to_dict()
        elif self.meta and isinstance(self.meta, dict):
            meta = self.meta

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job import Job
        from ..models.pagination_meta import PaginationMeta

        if not src_dict:
            return None
        d = src_dict.copy()
        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = Job.from_dict(data_item_data)

            data.append(data_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, PaginationMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = PaginationMeta.from_dict(_meta)

        job_list = cls(
            data=data,
            meta=meta,
        )

        job_list.additional_properties = d
        return job_list

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
