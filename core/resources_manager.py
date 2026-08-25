from __future__ import annotations
from pathlib import Path
from typing import final, ClassVar
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel, ConfigDict
from loguru import logger


@final
class ResourcesManager(BaseModel):

    model_config = ConfigDict(
        extra='ignore',
        frozen=False,
        validate_default=True,
    )

    DEFAULT_ENV_FILE: ClassVar[Path] = Path("config.env")

    TG_TOKEN: ClassVar[str]
    DB_URL: ClassVar[str]
    AI_API_KEY: ClassVar[str]
    AI_MODEL: ClassVar[str]

    @staticmethod
    def __load_env_config(env_path: Path) -> None:
        """
        Подгрузка переменных из env в код
        """
        if env_path.exists():
            load_dotenv(env_path)
        else:
            logger.warning("Предупреждение: файл окружения не найден")

    @classmethod
    def load_config(cls, env_path: Path = DEFAULT_ENV_FILE) -> None:
        """
        Загружает конфигурацию из .env
        """
        cls.__load_env_config(env_path=env_path)

        cls.TG_TOKEN = getenv("TG_TOKEN", "")
        cls.DB_URL = getenv("DB_URL", "")
        cls.AI_API_KEY = getenv("AI_API_KEY", "")
        cls.AI_MODEL = getenv("AI_MODEL", "")
