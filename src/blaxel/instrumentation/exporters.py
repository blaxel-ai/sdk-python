from typing import Callable, Dict, Sequence

from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LogData
from opentelemetry.sdk.metrics.export import MetricExportResult, MetricsData


class DynamicHeadersSpanExporter(OTLPSpanExporter):
    """Span exporter with dynamic headers."""

    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        self._get_headers = get_headers
        super().__init__()

    def export(self, spans):
        self._session.headers.update(self._get_headers())
        return super().export(spans)

class DynamicHeadersMetricExporter(OTLPMetricExporter):
    """Metric exporter with dynamic headers."""

    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        self._get_headers = get_headers
        super().__init__()

    def export(
        self,
        metrics_data: MetricsData,
        timeout_millis: float = 10_000,
        **kwargs,
    ) -> MetricExportResult:
        self._session.headers.update(self._get_headers())
        return super().export(metrics_data, timeout_millis, **kwargs)

class DynamicHeadersLogExporter(OTLPLogExporter):
    """Log exporter with dynamic headers."""
    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        self._get_headers = get_headers
        super().__init__()

    def export(self, batch: Sequence[LogData]):
        self._session.headers.update(self._get_headers())
        return super().export(batch)