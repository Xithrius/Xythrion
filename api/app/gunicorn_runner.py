import logging
from typing import Any, ClassVar

import uvicorn
from gunicorn.glogging import Logger
from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app
from uvicorn.workers import UvicornWorker as BaseUvicornWorker

from app.settings import FILTER_LOG_ENDPOINTS, settings

try:
    import uvloop
except ImportError:
    uvloop = None

LOG_CONFIG = uvicorn.config.LOGGING_CONFIG

if settings.environment == "production":
    LOGGING_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"  # noqa: E501
    LOG_CONFIG["formatters"]["access"]["fmt"] = LOGGING_FORMAT


class UvicornWorker(BaseUvicornWorker):
    """
    Configuration for uvicorn workers.

    This class is subclassing UvicornWorker and defines
    some parameters class-wide, because it's impossible,
    to pass these parameters through gunicorn.
    """

    CONFIG_KWARGS: ClassVar = {
        "loop": "uvloop" if uvloop is not None else "asyncio",
        "http": "httptools",
        "lifespan": "on",
        "factory": True,
        "proxy_headers": False,
        "log_config": LOG_CONFIG,
    }


FILTER_LOGS = {f"GET {x} HTTP/1.1" for x in FILTER_LOG_ENDPOINTS}


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return all(record.getMessage().find(f) == -1 for f in FILTER_LOGS)


class CustomGunicornLogger(Logger):
    def setup(self, cfg: Any) -> None:
        super().setup(cfg)

        access_logger = logging.getLogger("gunicorn.access")
        access_logger.addFilter(EndpointFilter())


class GunicornApplication(BaseApplication):
    """
    Custom gunicorn application.

    This class is used to start guncicorn
    with custom uvicorn workers.
    """

    def __init__(
        self,
        app: str,
        host: str,
        port: int,
        workers: int,
        **kwargs: Any,
    ):
        self.options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": "app.gunicorn_runner.UvicornWorker",
            "logger_class": CustomGunicornLogger,
            **kwargs,
        }
        self.app = app
        super().__init__()

    def load_config(self) -> None:
        """
        Load config for web server.

        This function is used to set parameters to gunicorn
        main process. It only sets parameters that
        gunicorn can handle. If you pass unknown
        parameter to it, it crash with error.
        """
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self) -> str:
        """
        Load actual application.

        Gunicorn loads application based on this
        function's returns. We return python's path to
        the app's factory.

        :returns: python path to app factory.
        """
        return import_app(self.app)
