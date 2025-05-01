"""
This module provides utilities for setting up and managing OpenTelemetry instrumentation within Blaxel.
It includes classes and functions for configuring tracers, meters, loggers, and integrating with FastAPI applications.
"""

import importlib
import logging
import signal
import time
from typing import Any, Dict, List, Optional, Type

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.metrics import NoOpMeterProvider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import NoOpTracerProvider

from blaxel.instrumentation.exporters import (
    DynamicHeadersLogExporter,
    DynamicHeadersMetricExporter,
    DynamicHeadersSpanExporter,
)
from blaxel.instrumentation.span import DefaultAttributesSpanProcessor

from ..common.settings import Settings
from .log import AsyncLogRecordProcessor
from .map import MAPPINGS

logger = logging.getLogger(__name__)


class TelemetryManager:
    def __init__(self):
        self.tracer: Optional[trace.Tracer] = None
        self.meter: Optional[metrics.Meter] = None
        self.logger_provider: Optional[LoggerProvider] = None
        self.initialized: bool = False
        self.configured: bool = False
        self.settings: Settings = None

    @property
    def enabled(self) -> bool:
        return (self.settings and self.settings.enable_opentelemetry) or False

    @property
    def auth_headers(self) -> Dict[str, str]:
        return (self.settings and self.settings.headers) or {}

    @property
    def resource_name(self) -> str:
        return (self.settings and self.settings.name) or ""

    @property
    def resource_workspace(self) -> str:
        return (self.settings and self.settings.workspace) or ""

    @property
    def resource_type(self) -> str:
        resource_type = (self.settings and self.settings.type) or ""
        if resource_type:
            return f"{resource_type}s"
        return ""

    def get_resource_attributes(self) -> Dict[str, Any]:
        resources = Resource.create()
        resources_dict: Dict[str, Any] = {}
        for key in resources.attributes:
            resources_dict[key] = resources.attributes[key]
        if self.resource_name:
            resources_dict["service.name"] = self.resource_name
            resources_dict["workload.id"] = self.resource_name
        if self.resource_workspace:
            resources_dict["workspace"] = self.resource_workspace
        if self.resource_type:
            resources_dict["workload.type"] = self.resource_type
        return resources_dict

    def get_metrics_exporter(self) -> Optional[DynamicHeadersMetricExporter]:
        if not self.enabled:
            return None
        return DynamicHeadersMetricExporter(get_headers=lambda: self.auth_headers)

    def get_span_exporter(self) -> Optional[DynamicHeadersSpanExporter]:
        if not self.enabled:
            return None
        return DynamicHeadersSpanExporter(get_headers=lambda: self.auth_headers)

    def get_log_exporter(self) -> Optional[DynamicHeadersLogExporter]:
        if not self.enabled:
            return None
        return DynamicHeadersLogExporter(get_headers=lambda: self.auth_headers)

    def _import_class(self, module_path: str, class_name: str) -> Optional[Type]:
        """Dynamically import a class from a module path."""
        try:
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            logger.error(f"Could not import {class_name} from {module_path}: {str(e)}")
            return None

    def _is_package_installed(self, package_names: List[str]) -> bool:
        """Check if a package is installed."""
        for package_name in package_names:
            try:
                importlib.import_module(package_name)
            except (ImportError, ModuleNotFoundError):
                return False
        return True

    def setup_signal_handler(self):
        """Set up signal handlers for graceful shutdown."""
        def handle_signal(signum, frame):
            logger.debug(f"Received signal {signum}")
            self.shutdown()

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

    def initialize(self, settings: Settings):
        """Initialize the telemetry system."""
        self.settings = settings
        if not self.enabled or self.initialized:
            return

        self.setup_signal_handler()
        self.instrument()
        self.initialized = True
        logger.debug("Telemetry initialized")

    def instrument(self):
        """Set up OpenTelemetry instrumentation."""
        if not self.enabled:
            # Use NoOp implementations to stub tracing and metrics
            trace.set_tracer_provider(NoOpTracerProvider())
            self.tracer = trace.get_tracer(__name__)

            metrics.set_meter_provider(NoOpMeterProvider())
            self.meter = metrics.get_meter(__name__)
            return

        resource = Resource.create(self.get_resource_attributes())

        # Set up the TracerProvider
        trace_provider = TracerProvider(resource=resource)
        span_processor = BatchSpanProcessor(self.get_span_exporter())
        trace_provider.add_span_processor(DefaultAttributesSpanProcessor({
            "workload.id": self.resource_name,
            "workload.type": self.resource_type,
            "workspace": self.resource_workspace,
        }))
        trace_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(trace_provider)
        self.tracer = trace_provider.get_tracer(__name__)

        # Set up the MeterProvider
        metrics_exporter = PeriodicExportingMetricReader(self.get_metrics_exporter())
        meter_provider = MeterProvider(resource=resource, metric_readers=[metrics_exporter])
        metrics.set_meter_provider(meter_provider)
        self.meter = meter_provider.get_meter(__name__)

        # Set up the LoggerProvider
        self.logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(self.logger_provider)
        self.logger_provider.add_log_record_processor(
            AsyncLogRecordProcessor(self.get_log_exporter())
        )
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=self.logger_provider)
        logging.getLogger().addHandler(handler)

        # Load and enable instrumentations
        for name, mapping in MAPPINGS.items():
            if self._is_package_installed(mapping.required_packages):
                instrumentor_class = self._import_class(mapping.module_path, mapping.class_name)
                if instrumentor_class:
                    try:
                        instrumentor_class().instrument()
                        logger.debug(f"Successfully instrumented {name}")
                    except Exception as e:
                        logger.debug(f"Failed to instrument {name}: {str(e)}")
                else:
                    logger.debug(f"Could not load instrumentor for {name}")
            else:
                logger.debug(
                    f"Skipping {name} instrumentation - required package '{mapping.required_packages}' not installed"
                )

    def shutdown(self):
        """Shutdown the telemetry system gracefully with a 5-second timeout."""
        try:
            start_time = time.time()
            timeout = 5.0  # 5 seconds timeout

            if self.tracer:
                trace_provider = trace.get_tracer_provider()
                if isinstance(trace_provider, TracerProvider):
                    if time.time() - start_time < timeout:
                        trace_provider.shutdown()

            if self.meter:
                meter_provider = metrics.get_meter_provider()
                if isinstance(meter_provider, MeterProvider):
                    if time.time() - start_time < timeout:
                        meter_provider.shutdown()

            if self.logger_provider:
                if time.time() - start_time < timeout:
                    self.logger_provider.shutdown()

            if time.time() - start_time < timeout:
                logger.debug("Instrumentation shutdown complete")
            else:
                logger.warning("Shutdown timed out after 5 seconds, skipping remaining shutdown tasks")

        except Exception as error:
            logger.error(f"Error during shutdown: {error}")

# Create a singleton instance
telemetry_manager = TelemetryManager()
