import logging
import queue
import threading
from typing import Optional

from opentelemetry.context import attach, create_key, detach, set_value
from opentelemetry.sdk._logs import LogData, LogRecordProcessor
from opentelemetry.sdk._logs._internal.export import LogExporter

_logger = logging.getLogger(__name__)

class AsyncLogRecordProcessor(LogRecordProcessor):
    """This is an implementation of LogRecordProcessor which passes
    received logs in the export-friendly LogData representation to the
    configured LogExporter asynchronously using a background thread.
    """

    def __init__(self, exporter: LogExporter):
        self._exporter = exporter
        self._shutdown = False
        self._queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._start_worker()

    def _start_worker(self):
        """Start the background worker thread."""
        self._worker_thread = threading.Thread(
            target=self._process_logs,
            daemon=True,
            name="LogExporterWorker"
        )
        self._worker_thread.start()

    def _process_logs(self):
        """Process logs from the queue in the background thread."""
        while not self._shutdown:
            try:
                log_data = self._queue.get(timeout=1.0)
                token = attach(set_value(create_key("suppress_instrumentation"), True))
                try:
                    self._exporter.export((log_data,))
                except Exception:  # pylint: disable=broad-exception-caught
                    _logger.exception("Exception while exporting logs.")
                finally:
                    detach(token)
                    self._queue.task_done()
            except queue.Empty:
                continue

    def emit(self, log_data: LogData):
        if self._shutdown:
            _logger.warning("Processor is already shutdown, ignoring call")
            return
        self._queue.put(log_data)

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
