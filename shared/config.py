import os
import pathlib
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
from pydantic import Field, PostgresDsn, computed_field


BASE_DIRPATH = str(pathlib.Path(__file__).parent.parent)


class DatabaseSettings(BaseSettings):
    """Настройки базы данных."""
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """Создает URL для подключения к базе данных."""
        return str(PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        ))

    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> PostgresDsn:
        """Создает асинхронный URL для подключения к базе данных."""
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        ))

    class Config:
        env_file = os.path.join(BASE_DIRPATH, "database_settings.env")
        env_file_encoding = "utf-8"
        case_sensitive = True


class AdminSettings(BaseSettings):
    """Настройки административной панели."""
    
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    SECRET_KEY: str

    class Config:
        env_file = os.path.join(BASE_DIRPATH, "admin_settings.env")
        env_file_encoding = "utf-8"
        case_sensitive = True


class BotSettings(BaseSettings):
    """Настройки телеграм бота."""
    
    BOT_TOKEN: str
    ADMIN_IDS: List[int]

    class Config:
        env_file = os.path.join(BASE_DIRPATH, "bot_settings.env")
        env_file_encoding = "utf-8"
        case_sensitive = True


class Settings(BaseSettings):
    """Основные настройки приложения."""
    
    database: DatabaseSettings = DatabaseSettings()
    admin: AdminSettings = AdminSettings()
    bot: BotSettings = BotSettings()
    BASE_DIRPATH: str = BASE_DIRPATH


@lru_cache(maxsize=1)
def get_cached_settings() -> Settings:
    """Получение кэшированных настроек приложения."""
    return Settings()