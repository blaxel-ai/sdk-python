Module blaxel.telemetry.log.log
===============================

Classes
-------

`AsyncLogRecordProcessor(exporter: opentelemetry.sdk._logs._internal.export.LogExporter)`
:   This is an implementation of LogRecordProcessor which passes
    received logs in the export-friendly LogData representation to the
    configured LogExporter asynchronously using a background thread.

    ### Ancestors (in MRO)

    * opentelemetry.sdk._logs._internal.LogRecordProcessor
    * abc.ABC

    ### Methods

    `emit(self, log_data: opentelemetry.sdk._logs._internal.LogData)`
    :   Emits the `LogData`

    `force_flush(self, timeout_millis: int = 500) ‑> bool`
    :   Wait for all pending exports to complete.

    `shutdown(self)`
    :   Shutdown the processor and wait for pending exports to complete.