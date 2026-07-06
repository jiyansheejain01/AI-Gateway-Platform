"""
Centralized application configuration.

Loads all settings from the .env file using pydantic-settings.
Every service should import the shared `settings` object instead
of hardcoding configuration values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================================================
    # APP
    # ==========================================================
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

    # ==========================================================
    # EXECUTION MODE
    # ==========================================================

    LOCAL_MODE: bool

    SQLITE_PATH: str

    QDRANT_PATH: str

    # ==========================================================
    # JWT
    # ==========================================================
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    # ==========================================================
    # REDIS
    # ==========================================================
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # ==========================================================
    # POSTGRES
    # ==========================================================
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ==========================================================
    # KAFKA
    # ==========================================================
    KAFKA_BOOTSTRAP_SERVERS: str
    RESPONSE_TOPIC: str

    # ==========================================================
    # QDRANT
    # ==========================================================
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str

    # ==========================================================
    # OLLAMA
    # ==========================================================

    OLLAMA_BASE_URL: str

    LLAMA_MODEL: str
    PHI3_MODEL: str

    # ==========================================================
    # RATE LIMITER
    # ==========================================================
    RATE_LIMIT: int
    RATE_LIMIT_WINDOW: int

    # ==========================================================
    # MONITORING
    # ==========================================================
    TEMPO_ENDPOINT: str
    LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def DATABASE_URL(self) -> str:

        if self.LOCAL_MODE:
            return f"sqlite:///{self.SQLITE_PATH}"

        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()