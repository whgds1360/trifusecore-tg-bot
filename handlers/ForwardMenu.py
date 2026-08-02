from aiogram import Router, types, F, Bot
from aiogram.types import InaccessibleMessage
from aiogram.fsm.context import FSMContext

from database.DataBase import DataBase
from sqlalchemy import select

from bot.KeyboardCreator import KeyboardCreator
from forward.ForwardManager import ForwardManager
from states.StatesManager import StatesManager

from typing import Dict
from loguru import logger
from asyncio import create_task, Task

forward_menu_router = Router()
active_listeners: Dict[int, Task] = {}


@forward_menu_router.callback_query(F.data == "begin_forward")
async def begin_forward(callback: types.CallbackQuery, bot: Bot) -> None:
    if not callback.message or isinstance(callback.message,
                                          InaccessibleMessage):

        await callback.answer("Сообщение недоступно", show_alert=True)
        return

    chat_id = callback.message.chat.id

    if chat_id in active_listeners:

        await callback.answer(text="❗У вас уже включена пересылка❗", show_alert=True)
        return

    users = DataBase.get_users()

    try:
        with DataBase.get_sessionmaker()() as session:

            user = session.scalar(select(users).where(users.tg_id == chat_id)) #type: ignore

            if not user:

                await callback.message.answer(text="❌ Пользователь не найден!")
                await callback.answer()
                return

            if user.is_active_forward == "1": #type: ignore

                await callback.message.answer(text="❗У вас уже включена пересылка❗", show_alert=True)
                return

            if not user.forward_config: #type: ignore

                await callback.message.answer(text="❌ Конфиг не найден!")
                await callback.answer()
                return

            ready_config = parse_config(user.forward_config) #type: ignore

            if ('VK_TOKEN' not in ready_config
                or 'VK_COMMUNITY_TOKEN' not in ready_config
                    or 'LIST_OF_LISTEN' not in ready_config):

                await callback.message.answer(text="❌ В конфиге отсутствуют обязательные поля!")
                await callback.answer()
                return

            user.is_active_forward = "1"
            session.commit()

            task = create_task(
                ForwardManager.vk_listener(
                    bot=bot,
                    chat_id=callback.message.chat.id,
                    vk_token=ready_config["VK_TOKEN"],
                    vk_community_token=ready_config["VK_COMMUNITY_TOKEN"],
                    list_of_listen=ready_config["LIST_OF_LISTEN"],
                    active_listeners=active_listeners
                )
            )

            active_listeners[callback.message.chat.id] = task

            await callback.message.answer(text="✅ Пересылка включена!")

    except Exception as e:
        logger.error(f"Ошибка в begin_forward: {e}")
        await callback.message.answer(text=f"❌ Ошибка: {e}")

    await callback.answer()


@forward_menu_router.callback_query(F.data == "end_forward")
async def stop_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):
        chat_id = callback.message.chat.id

        if chat_id not in active_listeners:
            logger.debug(active_listeners)
            await callback.message.answer(text="❌ У вас не включена перессылка!")
            await callback.answer()
            return

        task = active_listeners.pop(chat_id, None)

        if task and not task.done():
            task.cancel()
            await callback.message.answer(text="⏹️ Пересылка остановлена!")

            try:
                with DataBase.get_sessionmaker()() as session:
                    users = DataBase.get_users()
                    user = session.scalar(
                        select(users).where(users.tg_id == chat_id))  # type: ignore
                    if user:
                        user.is_active_forward = "0"
                        session.commit()
            except Exception as e:
                logger.error(f"Ошибка обновления статуса: {e}")
        else:
            await callback.message.answer(text="⚠️ Слушатель уже завершён!")

    await callback.answer()


@forward_menu_router.callback_query(F.data == "config_forward")
async def config_forward(callback: types.CallbackQuery,
                         state: FSMContext) -> None:
    if ((DataBase.get_engine()
        and DataBase.get_sessionmaker)
            and callback.message
            and not isinstance(callback.message, InaccessibleMessage)):

        users = DataBase.get_users()

        with DataBase.get_sessionmaker()() as session:

            response = session.scalar(select(users.have_forward_config).where(users.tg_id == callback.message.chat.id)) # type: ignore
            if response == "1":

                await callback.message.answer(text="У вас уже определен конфиг!")

            else:
                await callback.message.answer(text="Я готов принять конфиг, ❗ПИШИТЕ В СООТВЕСТВУЮЩЕМ ФОРМАТЕ как указано в разделе ИНФО❗")
                await state.set_state(StatesManager.waiting_for_config)

    await callback.answer()


@forward_menu_router.message(StatesManager.waiting_for_config)
async def post_forward_config(message: types.Message,
                              state: FSMContext) -> None:
    if ((DataBase.get_engine()
        and DataBase.get_sessionmaker)
            and message
            and not isinstance(message, InaccessibleMessage)):

        users = DataBase.get_users()

        if not message.text:

            await message.answer(text="Вы ввели неверный конфиг попробуйте еще раз!")
            return

        with DataBase.get_sessionmaker()() as session:

            user = session.scalar(select(users).where(users.tg_id == message.chat.id)) #type: ignore
            if user:
                user.forward_config = message.text
                user.have_forward_config = "1"

                session.commit()

                await message.answer(text="Конфиг успешно сохранен!")

    await state.clear()


@forward_menu_router.callback_query(F.data == "delete_forward_config")
async def delete_forward_config(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message, InaccessibleMessage):

        users = DataBase.get_users()
        with DataBase.get_sessionmaker()() as session:

            user = session.scalar(select(users).where(users.tg_id == callback.message.chat.id)) #type: ignore
            if user:

                if user.is_active_forward == "0": #type: ignore

                    user.forward_config = ""
                    user.have_forward_config = "0"

                    session.commit()

                    await callback.message.answer(text="Конфиг успешно удален!")
                else:

                    await callback.message.answer(text="Сначала остановите пересылку!")

    await callback.answer()


@forward_menu_router.callback_query(F.data == "back_forward")
async def back_main_menu(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):

        await callback.message.edit_text(text="Главное меню",
                                         reply_markup=KeyboardCreator.main_menu())

    await callback.answer()


@forward_menu_router.callback_query(F.data == "info_forward")
async def info_forward(callback: types.CallbackQuery) -> None:
    if callback.message and not isinstance(callback.message,
                                           InaccessibleMessage):

        await callback.message.answer(text="Пока нету")

    await callback.answer()


def parse_config(config_text: str) -> Dict[str, str]:
    """
    Парсит строку конфига с разделителем &
    Пример: LIST_OF_LISTEN=1,2,3&VK_TOKEN=token&VK_COMMUNITY_TOKEN=123
    Возвращает словарь с параметрами
    """
    config_dict = {}

    pairs = config_text.split('&')

    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            config_dict[key.strip()] = value.strip()
        else:
            continue

    return config_dict
