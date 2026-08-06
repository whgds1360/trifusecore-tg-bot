from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage

from database.DataBase import DataBase
from sqlalchemy import select

from bot.KeyboardCreator import KeyboardCreator
from mail.TempMailManager import TempMailManager
from text_config.TextConfigManager import TextConfigManager

from typing import Dict
from loguru import logger

temp_mail_menu_router = Router()
active_mails: Dict[int, TempMailManager] = {}


@temp_mail_menu_router.callback_query(F.data == "make_mail")
async def make_mail(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        try:
            with DataBase.get_sessionmaker()() as session:
                users = DataBase.get_users()

                user = session.scalar(
                    select(users).where(users.tg_id == callback.message.chat.id)  # type: ignore
                )

                user.use_temp_mail = "1"  # type: ignore
                session.commit()
        except Exception as error:
            logger.error(f"Ошибка изменения статуса пользования временной почтой: {error}")

        email = TempMailManager()
        if email:
            active_mails[callback.message.chat.id] = email
            await callback.message.answer(text=f"Ваша почта: {email.email.email}")
        else:
            logger.error("Прилетела пустая почта")

    await callback.answer()


@temp_mail_menu_router.callback_query(F.data == "get_mails")
async def get_mails(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        email = active_mails.get(callback.message.chat.id, None)
        if email:
            msg = email.get_inbox()
            if not msg:
                await callback.answer(text="❗У вас нет входящих сообщений❗")
            else:
                await callback.message.answer(text=f"Список писем:\n{msg}", parse_mode=None)
        else:
            await callback.answer(text="❗У вас нет активной временной почты, создай её❗", show_alert=True)

    await callback.answer()


@temp_mail_menu_router.callback_query(F.data == "info_temp_mail")
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.answer(text=TextConfigManager.config["temp_mail_info"])

    await callback.answer()


@temp_mail_menu_router.callback_query(F.data == "back_temp_mail")
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(text="Главное меню",
                                         reply_markup=KeyboardCreator.main_menu())

    await callback.answer()
