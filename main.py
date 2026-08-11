from core.resources_manager import ResourcesManager
from core.text_config_manager import TextConfigManager

from asyncio import run

from loguru import logger

if __name__ == "__main__":
    try:
        ResourcesManager.load_config()
        TextConfigManager.load_config()

        from core.сore import Core
        run(Core.initialization_tg_bot())

    except Exception as error:
        logger.error(f"Ошибка инициализации бота: {error}")
