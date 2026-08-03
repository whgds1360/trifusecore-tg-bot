from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage

from ai.AiManager import AiManager
from bot.KeyboardCreator import KeyboardCreator

from database.DataBase import DataBase
from sqlalchemy import select

from loguru import logger


ai_menu_router = Router()


@ai_menu_router.callback_query(F.data == "change_mod_request")
async def change_mod_request(callback: types.CallbackQuery) -> None:
    if (callback.message
        and not isinstance(callback.message, InaccessibleMessage)
            and callback.message.text):
        try:
            response = await AiManager.get_response(content=callback.message.text)
            if response:
                await callback.message.answer(text=response)
            try:
                with DataBase.get_sessionmaker()() as session:
                    users = DataBase.get_users()

                    user = session.scalar(
                        select(users).where(users.tg_id == callback.message.chat.id)  # type: ignore
                    )

                    if user:
                        user.use_ai == "1"  # type: ignore

                        session.commit()
            except Exception as error:
                logger.error(f"Ошибка записи статуса использования ai в БД: {error}")
        except Exception as error:
            logger.error(f"Ошибка при работе с нейронкой: {error}")

    await callback.answer()


@ai_menu_router.callback_query(F.data == "change_mod_photo")
async def change_mod_photo(callback: types.CallbackQuery) -> None:
    if (callback.message
        and not isinstance(callback.message, InaccessibleMessage)
            and callback.message.text):
        await callback.answer(text="⚙️Скоро добавим", show_alert=True)

    await callback.answer()


@ai_menu_router.callback_query(F.data == "info_ai_mod")
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.answer(text="Пока нету")

    await callback.answer()


@ai_menu_router.callback_query(F.data == "back_ai_mod")
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(text="Главное меню",
                                         reply_markup=KeyboardCreator.main_menu())

    await callback.answer()
