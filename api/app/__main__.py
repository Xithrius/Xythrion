import uvicorn

from .gunicorn_runner import GunicornApplication
from .settings import settings


def main() -> None:
    """Entrypoint of the application."""
    if settings.reload:
        uvicorn.run(
            "app.routers.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.value.lower(),
            factory=True,
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
