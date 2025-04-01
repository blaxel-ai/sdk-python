"""
This module provides utilities for creating and managing OpenTelemetry spans within Blaxel.
It includes classes for adding default attributes to spans and managing span creation.
"""

from typing import Any, ContextManager, Dict, Optional, TypeVar

from opentelemetry import trace
from opentelemetry.sdk.trace import Span as SdkSpan
from opentelemetry.sdk.trace.export import SpanProcessor
from opentelemetry.trace import Span, Tracer

from ..common.settings import settings

T = TypeVar('T')


class DefaultAttributesSpanProcessor(SpanProcessor):
    """A span processor that adds default attributes to spans when they are created."""

    def __init__(self, default_attributes: Dict[str, str]):
        self.default_attributes = default_attributes

    def on_start(self, span: SdkSpan, parent_context = None) -> None:
        """Add default attributes to the span when it starts."""
        for key, value in self.default_attributes.items():
            span.set_attribute(key, value)

    def on_end(self, span: SdkSpan) -> None:
        """Called when a span ends."""
        pass

    def shutdown(self) -> None:
        """Shuts down the span processor."""
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Forces the span processor to flush any queued spans."""
        return True


class SpanManager:
    """Manages the creation and lifecycle of spans."""

    def __init__(self, name: str):
        self.tracer: Tracer = trace.get_tracer(name)

    def create_active_span(self, name: str, attributes: Dict[str, Any], parent: Optional[Span] = None) -> ContextManager[Span]:
        """
        Creates an active span and executes the provided function within its context.

        Args:
            name: The name of the span
            attributes: Attributes to add to the span
            parent: Optional parent span

        Returns:
            Context manager that yields the span
        """
        # Add default attributes
        attributes["blaxel.environment"] = settings.env
        attributes["workload.id"] = settings.name
        attributes["workload.type"] = f"{settings.type}s"
        attributes["workspace"] = settings.workspace
        context = None
        if parent:
            context = trace.set_span_in_context(parent)
        return self.tracer.start_as_current_span(name, attributes=attributes, context=context)

    def create_span(self, name: str, attributes: Dict[str, Any], parent: Optional[Span] = None) -> Span:
        """
        Creates a new span without making it active.

        Args:
            name: The name of the span
            attributes: Attributes to add to the span
            parent: Optional parent span

        Returns:
            The created span
        """
        # Add default attributes
        full_attributes = {
            **attributes,
            "blaxel.environment": settings.env,
            "workload.id": settings.name,
            "workload.type": f"{settings.type}s",
            "workspace": settings.workspace
        }

        context = None
        if parent:
            context = trace.set_span_in_context(parent)
        return self.tracer.start_span(name, attributes=full_attributes, context=context)
