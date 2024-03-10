import logging
import os
import shutil

import uvicorn

from app.gunicorn_runner import GunicornApplication

from .settings import FILTER_LOG_ENDPOINTS, LOG_CONFIG, settings

FILTER_LOGS = {f"GET {x} HTTP/1.1" for x in FILTER_LOG_ENDPOINTS}


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return all(record.getMessage().find(f) == -1 for f in FILTER_LOGS)


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


def set_multiproc_dir() -> None:
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)

    os.makedirs(settings.prometheus_dir, exist_ok=True)

    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )


def main() -> None:
    set_multiproc_dir()

    if settings.reload:
        uvicorn.run(
            "app.routers.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            log_level=settings.log_level.value.lower(),
            factory=True,
            log_config=LOG_CONFIG,
        )
    else:
        GunicornApplication(
            "app.routers.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',
        ).run()


if __name__ == "__main__":
    main()
