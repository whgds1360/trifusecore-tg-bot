from loguru import logger
from sqlalchemy import select
from core.database import DataBase
from core.states_manager import StatesManager
from core.text_config_manager import TextConfigManager
from core.keyboard_creator import KeyboardCreator
from features.ai_chat.ai_manager import AiManager
from aiogram_sentinel import rate_limit, debounce
from aiogram.fsm.context import FSMContext
from aiogram.types import InaccessibleMessage
from aiogram import Router, types, F


ai_menu_router = Router()


@ai_menu_router.callback_query(F.data == "change_mod_request")
@rate_limit(1, 5)
@debounce(2)
async def change_mod_request(callback: types.CallbackQuery,
                             state: FSMContext) -> None:
    if (callback.message
            and not isinstance(callback.message, InaccessibleMessage)
            and callback.message.text):
        try:
            await callback.message.answer(text="Напиши свой вопрос😊😁")
            await state.set_state(StatesManager.wait_query_get_response_ai)
        except Exception as error:
            logger.error(
                f"Ошибка при смене состояния в change_mod_request: {error}")

    await callback.answer()


@ai_menu_router.message(StatesManager.wait_query_get_response_ai)
@rate_limit(1, 5)
@debounce(2)
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
                        select(users).where(users.tg_id ==
                                            message.chat.id)
                    )

                    if user:
                        user.use_ai = "1"

                        session.commit()
            except Exception as error:
                logger.error(
                    f"Ошибка записи статуса использования ai в БД: {error}")
        except Exception as error:
            logger.error(f"Ошибка при работе с нейронкой: {error}")

    await state.clear()


@ai_menu_router.callback_query(F.data == "change_mod_photo")
@rate_limit(1, 5)
@debounce(2)
async def change_mod_photo(callback: types.CallbackQuery) -> None:
    if (callback.message
        and not isinstance(callback.message, InaccessibleMessage)
            and callback.message.text):
        await callback.answer(text="⚙️Скоро добавим", show_alert=True)

    await callback.answer()


@ai_menu_router.callback_query(F.data == "info_ai_mod")
@rate_limit(1, 5)
@debounce(2)
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.answer(text=TextConfigManager.config["ai_info"])

    await callback.answer()


@ai_menu_router.callback_query(F.data == "back_ai_mod")
@rate_limit(1, 5)
@debounce(2)
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(text="Главное меню",
                                         reply_markup=KeyboardCreator.main_menu())

    await callback.answer()
