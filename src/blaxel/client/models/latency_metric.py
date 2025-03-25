from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.histogram_bucket import HistogramBucket
    from ..models.histogram_stats import HistogramStats


T = TypeVar("T", bound="LatencyMetric")


@_attrs_define
class LatencyMetric:
    """Latency metrics

    Attributes:
        global_histogram (Union[Unset, HistogramBucket]): Histogram bucket
        global_stats (Union[Unset, HistogramStats]): Histogram stats
        histogram_per_code (Union[Unset, HistogramBucket]): Histogram bucket
        stats_per_code (Union[Unset, HistogramStats]): Histogram stats
    """

    global_histogram: Union[Unset, "HistogramBucket"] = UNSET
    global_stats: Union[Unset, "HistogramStats"] = UNSET
    histogram_per_code: Union[Unset, "HistogramBucket"] = UNSET
    stats_per_code: Union[Unset, "HistogramStats"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        global_histogram: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.global_histogram
            and not isinstance(self.global_histogram, Unset)
            and not isinstance(self.global_histogram, dict)
        ):
            global_histogram = self.global_histogram.to_dict()
        elif self.global_histogram and isinstance(self.global_histogram, dict):
            global_histogram = self.global_histogram

        global_stats: Union[Unset, dict[str, Any]] = UNSET
        if self.global_stats and not isinstance(self.global_stats, Unset) and not isinstance(self.global_stats, dict):
            global_stats = self.global_stats.to_dict()
        elif self.global_stats and isinstance(self.global_stats, dict):
            global_stats = self.global_stats

        histogram_per_code: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.histogram_per_code
            and not isinstance(self.histogram_per_code, Unset)
            and not isinstance(self.histogram_per_code, dict)
        ):
            histogram_per_code = self.histogram_per_code.to_dict()
        elif self.histogram_per_code and isinstance(self.histogram_per_code, dict):
            histogram_per_code = self.histogram_per_code

        stats_per_code: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.stats_per_code
            and not isinstance(self.stats_per_code, Unset)
            and not isinstance(self.stats_per_code, dict)
        ):
            stats_per_code = self.stats_per_code.to_dict()
        elif self.stats_per_code and isinstance(self.stats_per_code, dict):
            stats_per_code = self.stats_per_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if global_histogram is not UNSET:
            field_dict["globalHistogram"] = global_histogram
        if global_stats is not UNSET:
            field_dict["globalStats"] = global_stats
        if histogram_per_code is not UNSET:
            field_dict["histogramPerCode"] = histogram_per_code
        if stats_per_code is not UNSET:
            field_dict["statsPerCode"] = stats_per_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.histogram_bucket import HistogramBucket
        from ..models.histogram_stats import HistogramStats

        if not src_dict:
            return None
        d = src_dict.copy()
        _global_histogram = d.pop("globalHistogram", UNSET)
        global_histogram: Union[Unset, HistogramBucket]
        if isinstance(_global_histogram, Unset):
            global_histogram = UNSET
        else:
            global_histogram = HistogramBucket.from_dict(_global_histogram)

        _global_stats = d.pop("globalStats", UNSET)
        global_stats: Union[Unset, HistogramStats]
        if isinstance(_global_stats, Unset):
            global_stats = UNSET
        else:
            global_stats = HistogramStats.from_dict(_global_stats)

        _histogram_per_code = d.pop("histogramPerCode", UNSET)
        histogram_per_code: Union[Unset, HistogramBucket]
        if isinstance(_histogram_per_code, Unset):
            histogram_per_code = UNSET
        else:
            histogram_per_code = HistogramBucket.from_dict(_histogram_per_code)

        _stats_per_code = d.pop("statsPerCode", UNSET)
        stats_per_code: Union[Unset, HistogramStats]
        if isinstance(_stats_per_code, Unset):
            stats_per_code = UNSET
        else:
            stats_per_code = HistogramStats.from_dict(_stats_per_code)

        latency_metric = cls(
            global_histogram=global_histogram,
            global_stats=global_stats,
            histogram_per_code=histogram_per_code,
            stats_per_code=stats_per_code,
        )

        latency_metric.additional_properties = d
        return latency_metric

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
