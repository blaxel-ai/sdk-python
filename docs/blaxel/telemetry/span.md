Module blaxel.telemetry.span
============================
This module provides utilities for creating and managing OpenTelemetry spans within Blaxel.
It includes classes for adding default attributes to spans and managing span creation.

Classes
-------

`DefaultAttributesSpanProcessor(default_attributes: Dict[str, str])`
:   A span processor that adds default attributes to spans when they are created.

    ### Ancestors (in MRO)

    * opentelemetry.sdk.trace.SpanProcessor

    ### Methods

    `force_flush(self, timeout_millis: int = 30000) ‑> bool`
    :   Forces the span processor to flush any queued spans.

    `on_end(self, span: opentelemetry.sdk.trace.Span) ‑> None`
    :   Called when a span ends.

    `on_start(self, span: opentelemetry.sdk.trace.Span, parent_context=None) ‑> None`
    :   Add default attributes to the span when it starts.

    `shutdown(self) ‑> None`
    :   Shuts down the span processor.

`SpanManager(name: str)`
:   Manages the creation and lifecycle of spans.

    ### Static methods

    `get_default_attributes() ‑> Dict[str, Any]`
    :   Get default attributes for the span.

    ### Methods

    `create_active_span(self, name: str, attributes: Dict[str, Any], parent: opentelemetry.trace.span.Span | None = None) ‑> ContextManager[opentelemetry.trace.span.Span]`
    :   Creates an active span and executes the provided function within its context.
        
        Args:
            name: The name of the span
            attributes: Attributes to add to the span
            parent: Optional parent span
        
        Returns:
            Context manager that yields the span

    `create_span(self, name: str, attributes: Dict[str, Any], parent: opentelemetry.trace.span.Span | None = None) ‑> opentelemetry.trace.span.Span`
    :   Creates a new span without making it active.
        
        Args:
            name: The name of the span
            attributes: Attributes to add to the span
            parent: Optional parent span
        
        Returns:
            The created span