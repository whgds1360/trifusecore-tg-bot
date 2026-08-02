from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InaccessibleMessage

from database.DataBase import DataBase
from sqlalchemy import select

from bot.KeyboardCreator import KeyboardCreator

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    if ((DataBase.get_engine()
        and DataBase.get_sessionmaker)
            and message
            and not isinstance(message, InaccessibleMessage)):

        users = DataBase.get_users()
        with DataBase.get_sessionmaker()() as session:

            response = session.scalar(
                select(users).where(users.tg_id == message.chat.id))  # type: ignore

            if response:
                await message.answer("С возращением!")
            else:
                new_user = users(tg_id=message.chat.id)

                session.add(new_user)
                session.commit()

                await message.answer("Привет! Вижу ты новенький, обязательно прочитай инфо!")

    await message.answer(text="Главное меню", reply_markup=KeyboardCreator.main_menu())
