Module blaxel.telemetry.exporters
=================================

Classes
-------

`DynamicHeadersLogExporter(get_headers: Callable[[], Dict[str, str]])`
:   Log exporter with dynamic headers.

    ### Ancestors (in MRO)

    * opentelemetry.exporter.otlp.proto.http._log_exporter.OTLPLogExporter
    * opentelemetry.sdk._logs._internal.export.LogExporter
    * abc.ABC

    ### Methods

    `export(self, batch: Sequence[opentelemetry.sdk._logs._internal.LogData])`
    :   Exports a batch of logs.
        
        Args:
            batch: The list of `LogData` objects to be exported
        
        Returns:
            The result of the export

`DynamicHeadersMetricExporter(get_headers: Callable[[], Dict[str, str]])`
:   Metric exporter with dynamic headers.

    ### Ancestors (in MRO)

    * opentelemetry.exporter.otlp.proto.http.metric_exporter.OTLPMetricExporter
    * opentelemetry.sdk.metrics._internal.export.MetricExporter
    * abc.ABC
    * opentelemetry.exporter.otlp.proto.common._internal.metrics_encoder.OTLPMetricExporterMixin

    ### Methods

    `export(self, metrics_data: opentelemetry.sdk.metrics._internal.point.MetricsData, timeout_millis: float = 10000, **kwargs) ‑> opentelemetry.sdk.metrics._internal.export.MetricExportResult`
    :   Exports a batch of telemetry data.
        
        Args:
            metrics: The list of `opentelemetry.sdk.metrics.export.Metric` objects to be exported
        
        Returns:
            The result of the export

`DynamicHeadersSpanExporter(get_headers: Callable[[], Dict[str, str]])`
:   Span exporter with dynamic headers.

    ### Ancestors (in MRO)

    * opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter
    * opentelemetry.sdk.trace.export.SpanExporter

    ### Methods

    `export(self, spans)`
    :   Exports a batch of telemetry data.
        
        Args:
            spans: The list of `opentelemetry.trace.Span` objects to be exported
        
        Returns:
            The result of the export