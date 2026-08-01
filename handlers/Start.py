from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Бот успешно перезагружен")
