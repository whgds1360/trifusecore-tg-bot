from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.AllRouters import all_routers
from resources.ResourcesManager import ResourcesManager
from database.DataBase import DataBase

from loguru import logger


class Core:

    @staticmethod
    async def initialization_tg_bot():
        resources = ResourcesManager.load_config()
        DataBase.connect(db_url=resources.DB_URL)

        bot = Bot(token=resources.TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()

        dp.include_routers(*all_routers)
        logger.debug("Инициализация тг бота успешна!")

        await dp.start_polling(bot)
