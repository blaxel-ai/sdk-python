from unittest.mock import patch, MagicMock

import pytest
import requests

from blaxel.telemetry.exporters import (
    _DynamicHeadersSession,
    _OPENTELEMETRY_AVAILABLE,
    DynamicHeadersSpanExporter,
    DynamicHeadersMetricExporter,
    DynamicHeadersLogExporter,
)


class TestDynamicHeadersSession:
    def test_injects_headers_on_post(self):
        headers = {"Authorization": "Bearer token123", "X-Custom": "value"}
        session = _DynamicHeadersSession(get_headers=lambda: headers)

        with patch.object(requests.Session, "post", return_value=MagicMock()) as mock_post:
            session.post("http://example.com", data=b"test")

        assert session.headers["Authorization"] == "Bearer token123"
        assert session.headers["X-Custom"] == "value"
        mock_post.assert_called_once()

    def test_refreshes_headers_each_call(self):
        call_count = 0

        def get_headers():
            nonlocal call_count
            call_count += 1
            return {"X-Request-Id": str(call_count)}

        session = _DynamicHeadersSession(get_headers=get_headers)

        with patch.object(requests.Session, "post", return_value=MagicMock()):
            session.post("http://example.com", data=b"first")
            assert session.headers["X-Request-Id"] == "1"

            session.post("http://example.com", data=b"second")
            assert session.headers["X-Request-Id"] == "2"

        assert call_count == 2


@pytest.mark.skipif(not _OPENTELEMETRY_AVAILABLE, reason="opentelemetry not fully installed")
class TestDynamicHeadersExporters:
    def test_span_exporter_uses_dynamic_session(self):
        headers_fn = lambda: {"Authorization": "Bearer span-token"}
        exporter = DynamicHeadersSpanExporter(get_headers=headers_fn)
        assert isinstance(exporter._session, _DynamicHeadersSession)

    def test_metric_exporter_uses_dynamic_session(self):
        headers_fn = lambda: {"Authorization": "Bearer metric-token"}
        exporter = DynamicHeadersMetricExporter(get_headers=headers_fn)
        assert isinstance(exporter._session, _DynamicHeadersSession)

    def test_log_exporter_uses_dynamic_session(self):
        headers_fn = lambda: {"Authorization": "Bearer log-token"}
        exporter = DynamicHeadersLogExporter(get_headers=headers_fn)
        assert isinstance(exporter._session, _DynamicHeadersSession)
