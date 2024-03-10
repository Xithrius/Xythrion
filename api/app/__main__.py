import os
import shutil

import uvicorn

from .gunicorn_runner import GunicornApplication
from .settings import settings


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
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"  # noqa: E501
    )

    if settings.reload:
        uvicorn.run(
            "app.routers.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            log_level=settings.log_level.value.lower(),
            factory=True,
            log_config=log_config,
        )
    else:
        GunicornApplication(
            "app.routers.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            loglevel=settings.log_level.value.lower(),
            factory=True,
            log_config=log_config,
        ).run()


if __name__ == "__main__":
    main()
