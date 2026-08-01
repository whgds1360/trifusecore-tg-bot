from aiogram import Router, types, F
from aiogram.types import InaccessibleMessage
from aiogram.fsm.context import FSMContext

from database.DataBase import DataBase
from sqlalchemy import select

from bot.KeyboardCreator import KeyboardCreator

from states.StatesManager import StatesManager

forward_menu_router = Router()


@forward_menu_router.callback_query(F.data == "config_forward")
async def config_forward(callback: types.CallbackQuery, state: FSMContext) -> None:
    if ((DataBase.get_engine() and DataBase.get_sessionmaker) and callback.message and not isinstance(callback.message, InaccessibleMessage)):
        with DataBase.get_sessionmaker()() as session:
            users = DataBase.get_users()
            response = session.scalar(select(users.have_forward_config).where(users.tg_id == callback.message.chat.id)) # type: ignore
            if response == "1":
                await callback.message.answer(text="У вас уже определен конфиг!")
            else:
                await callback.message.answer(text="Я готов принять конфиг, ❗ПИШИТЕ В СООТВЕСТВУЮЩЕМ ФОРМАТЕ как указано в разделе ИНФО❗")
                await state.set_state(StatesManager.waiting_for_config)

    await callback.answer()
    
    
@forward_menu_router.message(StatesManager.waiting_for_config)
async def post_forward_config(message: types.Message, state: FSMContext):
    if ((DataBase.get_engine() and DataBase.get_sessionmaker) and callback.message and not isinstance(callback.message, InaccessibleMessage)):
        if not message.text:
            await message.answer(text="Вы ввели неверный конфиг попробуйте еще раз!")
            return
        
        with DataBase.get_sessionmaker()() as session:
            users = DataBase.get_users
            
            
        
        ready_data = parse_config(message.text)



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


def parse_config(config_text: str) -> dict:
    """
    Парсит строку конфига с разделителем &
    Пример: LIST_OF_LISTEN=1,2,3&VK_TOKEN=token&VK_COMMUNITY_TOKEN=123&CHAT_ID=456
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
