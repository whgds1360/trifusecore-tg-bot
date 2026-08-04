from resources.ResourcesManager import ResourcesManager
from text_config.TextConfigManager import TextConfigManager
from mail.TempMailManager import TempMailManager

from asyncio import run

from loguru import logger

if __name__ == "__main__":
    try:
        ResourcesManager.load_config()
        TextConfigManager.load_config()
        TempMailManager.init_client()

        from bot.Core import Core
        run(Core.initialization_tg_bot())

    except Exception as error:
        logger.error(f"Ошибка инициализации бота: {error}")
