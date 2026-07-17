from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from datetime import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_DIR = BASE_DIR / ".env"


class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    DB_URL: str

    TEST_DB_URL: str | None = None
    TEST_DB_ECHO: bool = False

    REDIS_URL: str
    SECRET_KEY: str
    ECHO: bool = False

    CLEANING_BUFFER_HOURS: int

    CHECK_IN_TIME: time = time(14, 0, 0)
    CHECK_OUT_TIME: time = time(12, 0, 0)

    model_config = SettingsConfigDict(
        env_file=ENV_DIR,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def CLEANING_BUFFER(self) -> timedelta:
        return timedelta(hours=self.CLEANING_BUFFER_HOURS)


settings = Settings()
