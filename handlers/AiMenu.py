from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage
from aiogram.fsm.context import FSMContext

from ai.AiManager import AiManager
from bot.KeyboardCreator import KeyboardCreator
from text_config.TextConfigManager import TextConfigManager
from states.StatesManager import StatesManager

from database.DataBase import DataBase
from sqlalchemy import select

from loguru import logger


ai_menu_router = Router()


@ai_menu_router.callback_query(F.data == "change_mod_request")
async def change_mod_request(callback: types.CallbackQuery,
                             state: FSMContext) -> None:
    if (callback.message
            and not isinstance(callback.message, InaccessibleMessage)
            and callback.message.text):
        try:
            await callback.message.answer(text="Напиши свой вопрос😊😁")
            await state.set_state(StatesManager.wait_query_get_response_ai)
        except Exception as error:
            logger.error(f"Ошибка при смене состояния в change_mod_request: {error}")

    await callback.answer()


@ai_menu_router.message(StatesManager.wait_query_get_response_ai)
async def wait_query_get_response_ai(message: types.Message,
                                     state: FSMContext) -> None:
    if (message
            and not isinstance(message, InaccessibleMessage)
            and message.text):
        try:
            response = await AiManager.get_response(content=message.text)
            if response:
                await message.answer(text=response)
            try:
                with DataBase.get_sessionmaker()() as session:
                    users = DataBase.get_users()

                    user = session.scalar(
                        select(users).where(users.tg_id == message.chat.id)  # type: ignore
                    )

                    if user:
                        user.use_ai = "1"  # type: ignore

                        session.commit()
            except Exception as error:
                logger.error(f"Ошибка записи статуса использования ai в БД: {error}")
        except Exception as error:
            logger.error(f"Ошибка при работе с нейронкой: {error}")

    await state.clear()


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
        await callback.message.answer(text=TextConfigManager.config["ai_info"])

    await callback.answer()


@ai_menu_router.callback_query(F.data == "back_ai_mod")
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(text="Главное меню",
                                         reply_markup=KeyboardCreator.main_menu())

    await callback.answer()
