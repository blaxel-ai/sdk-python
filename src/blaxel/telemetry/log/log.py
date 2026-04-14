import logging
import queue
import threading

from opentelemetry.context import attach, create_key, detach, set_value
from opentelemetry.sdk._logs import LogRecordProcessor
from opentelemetry.sdk._logs._internal.export import LogExporter

_logger = logging.getLogger(__name__)

# opentelemetry-sdk >=1.35 renamed emit(LogData) to on_emit(ReadWriteLogRecord)
# and removed the LogData class. Detect which API to use.
try:
    from opentelemetry.sdk._logs import LogData as _LogData

    _USE_LEGACY_EMIT = True
except ImportError:
    _USE_LEGACY_EMIT = False


class AsyncLogRecordProcessor(LogRecordProcessor):
    """This is an implementation of LogRecordProcessor which passes
    received logs to the configured LogExporter asynchronously using
    a background thread.
    """

    def __init__(self, exporter: LogExporter):
        self._exporter = exporter
        self._shutdown = False
        self._queue: queue.Queue = queue.Queue()
        self._worker_thread: threading.Thread | None = None
        self._start_worker()

    def _start_worker(self):
        """Start the background worker thread."""
        self._worker_thread = threading.Thread(
            target=self._process_logs, daemon=True, name="LogExporterWorker"
        )
        self._worker_thread.start()

    def _process_logs(self):
        """Process logs from the queue in the background thread."""
        while not self._shutdown:
            try:
                log_record = self._queue.get(timeout=1.0)
                token = attach(set_value(create_key("suppress_instrumentation"), True))
                try:
                    self._exporter.export((log_record,))
                except Exception:  # pylint: disable=broad-exception-caught
                    _logger.exception("Exception while exporting logs.")
                finally:
                    detach(token)
                    self._queue.task_done()
            except queue.Empty:
                continue

    def _enqueue(self, record):
        if self._shutdown:
            return
        self._queue.put(record)

    if _USE_LEGACY_EMIT:

        def emit(self, log_data: "_LogData"):
            self._enqueue(log_data)

    else:

        def on_emit(self, log_record, *args, **kwargs):
            self._enqueue(log_record)

    def shutdown(self):
        """Shutdown the processor and wait for pending exports to complete."""
        self._shutdown = True
        if self._worker_thread:
            self._worker_thread.join(timeout=5.0)
        self._exporter.shutdown()

    def force_flush(self, timeout_millis: int = 500) -> bool:
        """Wait for all pending exports to complete."""
        try:
            self._queue.join(timeout=timeout_millis)
            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False
