from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str | None = None
    prefix: str = "^"
    internal_api_url: str = "http://localhost:8001"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="XYTHRION_BOT_",
        env_file_encoding="utf-8",
    )


settings = Settings()
