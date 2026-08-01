from __future__ import annotations
from pathlib import Path
from typing import Final, final, ClassVar
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel, Field, ConfigDict
from loguru import logger


@final
class ResourcesManager(BaseModel):

    model_config = ConfigDict(
        extra='ignore',
        frozen=True,
        validate_default=True,
    )

    DEFAULT_ENV_FILE: ClassVar[Path] = Path("resources/config.env")

    TG_TOKEN: str = Field(default="", init=True, repr=False)
    DB_URL: str = Field(default="", init=True, repr=False)

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
    def load_config(cls, env_path: Path = DEFAULT_ENV_FILE) -> ResourcesManager:
        """
        Загружает конфигурацию из .env
        """
        cls.__load_env_config(env_path=env_path)

        tg_token = getenv("TG_TOKEN", "")
        db_url = getenv("DB_URL", "")

        data = {
            "TG_TOKEN": tg_token,
            "DB_URL": db_url
            }

        try:
            return cls.model_validate(data)
        except AttributeError:
            return cls()
