from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.AllRouters import all_routers
from resources.ResourcesManager import ResourcesManager


class Core:

    @classmethod
    def __load_main_requirements(cls):
        # Подгрузка конфига
        cls.resources = ResourcesManager.load_config()
        logger.debug("Конфигурацию загружена успешно!")

    @classmethod
    def __initialization_tg_bot(cls):
        cls.bot = Bot(token=cls.resources.TG_TOKEN,
                      default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        cls.dp = Dispatcher()
        cls.dp.include_routers(*all_routers)
        logger.debug("Инициализация тг бота успешна!")
