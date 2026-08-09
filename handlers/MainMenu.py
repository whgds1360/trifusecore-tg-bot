from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage
from aiogram.filters import Command
from aiogram_sentinel import rate_limit, debounce

from bot.KeyboardCreator import KeyboardCreator
from text_config.TextConfigManager import TextConfigManager


main_menu_router = Router()


@main_menu_router.message(Command("menu"))
@rate_limit(1, 10)
@debounce(5)
async def cmd_start(message: types.Message) -> None:
    await message.answer(text="Главное меню",
                         reply_markup=KeyboardCreator.main_menu())


@main_menu_router.callback_query(F.data == "forward_menu")
@rate_limit(1, 10)
@debounce(5)
async def show_forward_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, 
                                           InaccessibleMessage):
        await callback.message.edit_text(
            text="🔀 Меню пересылки",
            reply_markup=KeyboardCreator.forward_menu()
        )

    await callback.answer()


@main_menu_router.callback_query(F.data == "temp_mail_menu")
@rate_limit(1, 10)
@debounce(5)
async def temp_mail_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(
                text="🔀 Меню временной почты",
                reply_markup=KeyboardCreator.temp_mail_menu()
            )

    await callback.answer()


@main_menu_router.callback_query(F.data == "ai_menu")
@rate_limit(1, 10)
@debounce(5)
async def show_ai_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(
            text="🔀 Меню нейронки",
            reply_markup=KeyboardCreator.ai_mod_menu()
        )

    await callback.answer()


@main_menu_router.callback_query(F.data == "info_forward")
@rate_limit(1, 10)
@debounce(5)
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.answer(text=TextConfigManager.config["forward_info"])

    await callback.answer()


@main_menu_router.callback_query(F.data == "close")
@rate_limit(1, 10)
@debounce(5)
async def delete_menu(callback: types.CallbackQuery) -> None:
    await callback.answer()
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.delete()
