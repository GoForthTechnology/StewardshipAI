import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

def get_trace_id():
    """Helper to get the current trace ID in hex format."""
    span = trace.get_current_span()
    if span and span.get_span_context().is_valid:
        return format(span.get_span_context().trace_id, '032x')
    return None

def get_span_id():
    """Helper to get the current span ID in hex format."""
    span = trace.get_current_span()
    if span and span.get_span_context().is_valid:
        return format(span.get_span_context().span_id, '016x')
    return None

def setup_observability(app=None):
    """
    Sets up OpenTelemetry tracing with Google Cloud Trace exporter.
    Instruments FastAPI and HTTPX.
    """
    # Detect Service Name for Traces
    service_name = os.environ.get("OTEL_SERVICE_NAME", "stewardship-ai-api")
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })

    # Initialize Tracer Provider
    provider = TracerProvider(resource=resource)
    
    try:
        # Initialize Cloud Trace Exporter
        # This will use Application Default Credentials (ADC)
        exporter = CloudTraceSpanExporter()
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
        logging.info("OpenTelemetry: Cloud Trace exporter initialized.")
    except Exception as e:
        logging.error(f"OpenTelemetry: Failed to initialize Cloud Trace exporter: {e}")
        # Fallback to console or no-op if necessary (BatchSpanProcessor won't be added)

    trace.set_tracer_provider(provider)

    # Instrument Global Clients
    HTTPXClientInstrumentor().instrument()

    # Instrument FastAPI if provided
    if app:
        FastAPIInstrumentor.instrument_app(app)

    return trace.get_tracer("stewardship-ai")
