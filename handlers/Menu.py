from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage
from aiogram.filters import Command

from bot.KeyboardCreator import KeyboardCreator


menu_router = Router()


@menu_router.message(Command("menu"))
async def cmd_start(message: types.Message):
    await message.answer("Главное меню", reply_markup=KeyboardCreator.main_menu())


@menu_router.callback_query(F.data == "close")
async def delete_menu(callback: types.CallbackQuery):
    await callback.answer()
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        await callback.message.delete()
    else:
        pass
