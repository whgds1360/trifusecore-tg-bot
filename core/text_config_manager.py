from __future__ import annotations
from json import load, JSONDecodeError
from typing import final, Dict, ClassVar
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from loguru import logger


@final
class TextConfigManager(BaseModel):
    """Управляет загрузкой и хранением текстовых сообщений из JSON-конфига.

    Загружает конфигурационный файл config.json и предоставляет доступ
    к текстовым сообщениям для бота.

    Attributes:
        config: Словарь с текстовыми сообщениями из конфига.
    """

    model_config = ConfigDict(
        extra='ignore',
        frozen=False,
        validate_default=True,
    )

    config: ClassVar[Dict[str, str]] = Field(default={}, init=True, repr=True)

    @classmethod
    def load_config(cls, path: str = "config.json") -> None:
        """Загружает конфигурационный файл с текстами сообщений.

        Args:
            path: Путь к JSON-файлу конфигурации. По умолчанию 'config.json'.

        Raises:
            FileNotFoundError: Если файл не найден по указанному пути.
            JSONDecodeError: Если файл содержит некорректный JSON.
        """
        try:
            file_path = Path(path)

            if not file_path.exists():
                raise FileNotFoundError(f"Файл не найден: {path}")

            with open(file="config.json", encoding="utf8") as file:
                data = load(file)

            cls.config = data

        except JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            logger.error(f"Ошибка загрузки конфига: {e}")

    @classmethod
    def get_config(cls) -> Dict[str, str]:
        """Возвращает загруженный конфиг в виде словаря.

        Returns:
            Dict[str, str]: Словарь с текстовыми сообщениями.
                           Если конфиг не загружен, возвращает пустой словарь.
        """
        return cls.config if cls.config else {}
