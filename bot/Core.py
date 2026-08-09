import aiohttp
import ssl

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_sentinel import SentinelConfig, Sentinel

from handlers.AllRouters import all_routers
from resources.ResourcesManager import ResourcesManager
from database.DataBase import DataBase


from loguru import logger
from sqlalchemy import update
from typing import final


@final
class Core:
    @staticmethod
    def _patch_ssl() -> None:
        """
        Применяет патч для отключения проверки SSL сертификатов
        т.к. проблему с сертификатом я не решил
        """
        _old_create_connection = aiohttp.TCPConnector.__init__

        def _patched_init(self, *args, **kwargs):
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            kwargs['ssl'] = ssl_context
            return _old_create_connection(self, *args, **kwargs)

        aiohttp.TCPConnector.__init__ = _patched_init
        logger.info("✅ SSL патч применён")

    @staticmethod
    async def initialization_tg_bot() -> None:
        Core._patch_ssl()
        DataBase.connect(db_url=ResourcesManager.DB_URL)

        bot = Bot(token=ResourcesManager.TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()

        # https://pypi.org/project/aiogram-sentinel/
        config = SentinelConfig(
                    throttling_default_max=10,  # 10 messages per window
                    throttling_default_per_seconds=60,  # 60 second window
                    debounce_default_window=2,  # 2 second debounce
                    )

        sentinel_router, infra = await Sentinel.setup(dp, config)

        logger.debug("Инициализация тг бота успешна!")

        try:
            with DataBase.get_sessionmaker()() as session:
                users = DataBase.get_users()
                session.execute(
                    update(users).values(is_active_forward="0")
                )
                session.commit()
                logger.info("✅ Статусы пересылки сброшены при старте")
        except Exception as e:
            logger.error(f"❌ Ошибка сброса статусов: {e}")

        sentinel_router.include_routers(*all_routers)

        await dp.start_polling(bot)
