from __future__ import annotations
from json import load, JSONDecodeError
from typing import final, Dict, ClassVar
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from loguru import logger


@final
class TextConfigManager(BaseModel):

    model_config = ConfigDict(
        extra='ignore',
        frozen=False,
        validate_default=True,
    )

    config: ClassVar[Dict[str, str]] = Field(default={}, init=True, repr=True)

    @classmethod
    def load_config(cls, path: str = "config.json") -> None:
        try:
            file_path = Path(path)

            if not file_path.exists():
                raise FileNotFoundError(f"Файл не найден: {path}")

            with open(file="text_config/config.json", encoding="utf8") as file:
                data = load(file)

            cls.config = data

        except JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            logger.error(f"Ошибка загрузки конфига: {e}")

    @classmethod
    def get_config(cls) -> Dict[str, str]:
        return cls.config if cls.config else {}
