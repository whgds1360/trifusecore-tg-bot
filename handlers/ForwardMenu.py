from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage

from bot.KeyboardCreator import KeyboardCreator

forward_menu_router = Router()


@forward_menu_router.callback_query(F.data == "back_forward")
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        await callback.message.edit_text("Главное меню", reply_markup=KeyboardCreator.main_menu())

    await callback.answer()


@forward_menu_router.callback_query(F.data == "info_forward")
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        await callback.message.answer(text="Пока нету")

    await callback.answer()
