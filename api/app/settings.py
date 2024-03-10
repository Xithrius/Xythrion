import enum
from pathlib import Path
from tempfile import gettempdir

import uvicorn
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())
LOGGING_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"  # noqa: E501
LOG_CONFIG = uvicorn.config.LOGGING_CONFIG
LOG_CONFIG["formatters"]["access"]["fmt"] = LOGGING_FORMAT
FILTER_LOG_ENDPOINTS = {
    "/metrics",
    "/api/openapi.json",
    "/api/docs",
}


class LogLevel(str, enum.Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8001

    # quantity of workers for uvicorn
    workers_count: int = 1

    # Enable uvicorn reloading
    reload: bool = True

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "xythrion"
    db_pass: str = "xythrion"
    db_base: str = "xythrion"
    db_echo: bool = False

    # This variable is used to define
    # multiproc_dir. It's required for [uvi|guni]corn projects.
    prometheus_dir: Path = TEMP_DIR / "prom"

    # Grpc endpoint for opentelemetry.
    opentelemetry_endpoint: str | None = "http://localhost:4317"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="XYTHRION_API_",
        env_file_encoding="utf-8",
    )


settings = Settings()
