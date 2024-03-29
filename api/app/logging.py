import logging

import uvicorn

from app.settings import settings

FILTER_LOG_ENDPOINTS = {
    "/metrics",
    "/api/openapi.json",
    "/api/docs",
}
FILTER_LOGS = {f"GET {x} HTTP/1.1" for x in FILTER_LOG_ENDPOINTS}

LOG_CONFIG = uvicorn.config.LOGGING_CONFIG  # type: ignore config

if settings.environment == "production":
    LOGGING_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"  # noqa: E501
    LOG_CONFIG["formatters"]["access"]["fmt"] = LOGGING_FORMAT


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return all(record.getMessage().find(f) == -1 for f in FILTER_LOGS)
