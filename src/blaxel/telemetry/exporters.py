from __future__ import annotations

from typing import Callable, Dict, Sequence

try:
    import requests
    from opentelemetry.exporter.otlp.proto.http._log_exporter import (
        OTLPLogExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.sdk._logs import LogData
    from opentelemetry.sdk.metrics.export import MetricExportResult, MetricsData

    _OPENTELEMETRY_AVAILABLE = True
except ImportError:
    _OPENTELEMETRY_AVAILABLE = False
    OTLPLogExporter = object
    OTLPMetricExporter = object
    OTLPSpanExporter = object
    LogData = None
    MetricExportResult = None
    MetricsData = None


class _DynamicHeadersSession(requests.Session):
    """A requests.Session subclass that injects dynamic headers on every request."""

    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        super().__init__()
        self._get_headers = get_headers

    def post(self, *args, **kwargs):
        self.headers.update(self._get_headers())
        return super().post(*args, **kwargs)


class DynamicHeadersSpanExporter(OTLPSpanExporter):  # type: ignore[misc]
    """Span exporter with dynamic headers."""

    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        self._get_headers = get_headers
        session = _DynamicHeadersSession(get_headers)
        super().__init__(session=session)


class DynamicHeadersMetricExporter(OTLPMetricExporter):  # type: ignore[misc]
    """Metric exporter with dynamic headers."""

    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        self._get_headers = get_headers
        session = _DynamicHeadersSession(get_headers)
        super().__init__(session=session)


class DynamicHeadersLogExporter(OTLPLogExporter):  # type: ignore[misc]
    """Log exporter with dynamic headers."""

    def __init__(self, get_headers: Callable[[], Dict[str, str]]):
        self._get_headers = get_headers
        session = _DynamicHeadersSession(get_headers)
        super().__init__(session=session)
