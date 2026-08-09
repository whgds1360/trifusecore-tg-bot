from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InaccessibleMessage
from aiogram_sentinel import rate_limit, debounce

from database.DataBase import DataBase
from sqlalchemy import select

from bot.KeyboardCreator import KeyboardCreator

from loguru import logger

start_router = Router()


@start_router.message(Command("start"))
@rate_limit(1, 20)
@debounce(10)
async def cmd_start(message: types.Message):
    if ((DataBase.get_engine()
        and DataBase.get_sessionmaker)
            and message
            and not isinstance(message, InaccessibleMessage)):
        try:
            with DataBase.get_sessionmaker()() as session:
                users = DataBase.get_users()

                response = session.scalar(
                    select(users).where(users.tg_id == message.chat.id))  # type: ignore

                if response:
                    await message.answer("С возращением!")
                else:
                    new_user = users(tg_id=message.chat.id)

                    session.add(new_user)
                    session.commit()

                    await message.answer("Привет! Вижу ты новенький, обязательно прочитай инфо!")
        except Exception as error:
            logger.error(f"❗Ошибка записи нового пользователя в БД: {error}❗")

    await message.answer(text="Главное меню", reply_markup=KeyboardCreator.main_menu())
