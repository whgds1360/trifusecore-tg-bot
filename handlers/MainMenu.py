from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage
from aiogram.filters import Command

from bot.KeyboardCreator import KeyboardCreator


main_menu_router = Router()


@main_menu_router.message(Command("menu"))
async def cmd_start(message: types.Message) -> None:
    await message.answer("Главное меню", reply_markup=KeyboardCreator.main_menu())


@main_menu_router.callback_query(F.data == "forward_menu")
async def show_forward_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        await callback.message.edit_text(
            text="🔀 Меню пересылки",
            reply_markup=KeyboardCreator.forward_menu()
        )

    await callback.answer()


@main_menu_router.callback_query(F.data == "close")
async def delete_menu(callback: types.CallbackQuery) -> None:
    await callback.answer()
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        await callback.message.delete()
