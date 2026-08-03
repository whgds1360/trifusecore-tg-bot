from aiogram import Router, types, F, Bot
from aiogram.types import InaccessibleMessage
from aiogram.fsm.context import FSMContext

from database.DataBase import DataBase
from sqlalchemy import select

from bot.KeyboardCreator import KeyboardCreator
from forward.ForwardManager import ForwardManager
from states.StatesManager import StatesManager
from utils.UtilsManager import UtilsManager
from text_config.TextConfigManager import TextConfigManager

from typing import Dict
from loguru import logger
from asyncio import create_task, Task

forward_menu_router = Router()
active_listeners: Dict[int, Task] = {}


@forward_menu_router.callback_query(F.data == "begin_forward")
async def begin_forward(callback: types.CallbackQuery, bot: Bot) -> None:
    if callback.message and not isinstance(callback.message,
                                          InaccessibleMessage):
        chat_id = callback.message.chat.id

        if chat_id in active_listeners:
            await callback.answer(text="❗У вас уже включена пересылка❗", show_alert=True)
            return

        try:
            with DataBase.get_sessionmaker()() as session:
                users = DataBase.get_users() 
                user = session.scalar(
                        select(users).where(users.tg_id == chat_id)) #type: ignore

                if user:
                    if user.is_active_forward == "1": #type: ignore
                        await callback.answer(text="❗У вас уже включена пересылка❗", show_alert=True)
                        return

                    if not user.forward_config: #type: ignore
                        await callback.answer(text="❗У вас не настроен конфиг❗", show_alert=True)
                        return

                    ready_config = UtilsManager.parse_config_for_forward(user.forward_config) #type: ignore

                    if ('VK_TOKEN' not in ready_config
                        or 'VK_COMMUNITY_TOKEN' not in ready_config
                            or 'LIST_OF_LISTEN' not in ready_config):

                        await callback.answer(text="❗ В конфиге отсутствуют обязательные поля!❗", show_alert=True)
                        return

                    user.is_active_forward = "1" #type: ignore
                    session.commit()

                    task = create_task(
                        ForwardManager.vk_listener(
                            bot=bot,
                            chat_id=callback.message.chat.id,
                            vk_token=ready_config["VK_TOKEN"],
                            vk_community_token=ready_config["VK_COMMUNITY_TOKEN"],
                            active_listeners=active_listeners
                        )
                    )

                    active_listeners[callback.message.chat.id] = task

                    await callback.answer(text="✅ Пересылка включена!", show_alert=True)

        except Exception as e:
            logger.error(f"Ошибка в начале перессылки: {e}")
            await callback.answer(text=f"❌ Ошибка: {e}", show_alert=True)

    await callback.answer()


@forward_menu_router.callback_query(F.data == "end_forward")
async def stop_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        chat_id = callback.message.chat.id

        if chat_id not in active_listeners:
            await callback.answer(text="❌ У вас не включена перессылка!", show_alert=True)
            return

        task = active_listeners.pop(chat_id, None)

        if task and not task.done():
            task.cancel()
            await callback.answer(text="⏹️ Пересылка остановлена!", show_alert=True)

            try:
                with DataBase.get_sessionmaker()() as session:
                    users = DataBase.get_users()

                    user = session.scalar(
                        select(users).where(users.tg_id == chat_id))  # type: ignore

                    if user:
                        user.is_active_forward = "0"
                        session.commit()

            except Exception as error:
                logger.error(f"Ошибка остановки перессылки: {error}")
        else:
            await callback.answer(text="⚠️ Слушатель уже завершён!", show_alert=True)

    await callback.answer()


@forward_menu_router.callback_query(F.data == "config_forward")
async def config_forward(callback: types.CallbackQuery,
                         state: FSMContext) -> None:
    if ((DataBase.get_engine()
        and DataBase.get_sessionmaker)
            and callback.message
            and not isinstance(callback.message, InaccessibleMessage)):

        with DataBase.get_sessionmaker()() as session:
            users = DataBase.get_users()

            response = session.scalar(select(users.have_forward_config).where(users.tg_id == callback.message.chat.id)) # type: ignore
            if response == "1":
                await callback.answer(text="❗У вас уже определен конфиг❗", show_alert=True)

            else:
                await callback.message.answer(text="✅Я готов принять конфиг,❗ПИШИТЕ В ФОРМАТЕ как указано в разделе ИНФО❗")
                await state.set_state(StatesManager.waiting_for_config)

    await callback.answer()


@forward_menu_router.message(StatesManager.waiting_for_config)
async def post_forward_config(message: types.Message,
                              state: FSMContext) -> None:
    if ((DataBase.get_engine()
        and DataBase.get_sessionmaker)
            and message
            and not isinstance(message, InaccessibleMessage)):

        if not message.text:
            await message.answer(text="❗Вы ввели неверный конфиг, попробуйте еще раз!❗")
            return
        try:
            with DataBase.get_sessionmaker()() as session:
                users = DataBase.get_users()

                user = session.scalar(select(users).where(users.tg_id == message.chat.id)) #type: ignore
                if user:
                    user.forward_config = message.text
                    user.have_forward_config = "1"

                    session.commit()

                    await message.answer(text="✅Конфиг успешно сохранен!")

        except Exception as error:
            logger.error(f"Ошибка сохранения конфига в БД: {error}")

    await state.clear()


@forward_menu_router.callback_query(F.data == "delete_forward_config")
async def delete_forward_config(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        try:
            with DataBase.get_sessionmaker()() as session:
                users = DataBase.get_users()

                user = session.scalar(select(users).where(users.tg_id == callback.message.chat.id)) #type: ignore
                if user:

                    if user.is_active_forward == "0": #type: ignore

                        user.forward_config = ""
                        user.have_forward_config = "0"

                        session.commit()

                        await callback.message.answer(text="✅Конфиг успешно удален!")

                    else:
                        await callback.answer(text="❗Сначала остановите пересылку❗", show_alert=True)

        except Exception as error:
            logger.error(f"Ошибка удаления конфига из БД: {error}")

    await callback.answer()


@forward_menu_router.callback_query(F.data == "main_info")
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.answer(text=TextConfigManager.config["main_info"])

    await callback.answer()


@forward_menu_router.callback_query(F.data == "back_forward")
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):
        await callback.message.edit_text(text="Главное меню",
                                         reply_markup=KeyboardCreator.main_menu())

    await callback.answer()
