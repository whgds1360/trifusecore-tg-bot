from aiogram import Router, types
from aiogram import F
from bot import KeyboardCreator
from aiogram.filters import Command

menu_router = Router()

@menu_router.message(Command("menu"))
async def cmd_start(message: types.Message):
    await message.answer("Главное меню", KeyboardCreator.main_menu())

@menu_router.callback_query(F.data == "close")
async def delete_menu(callback: types.CallbackQuery):
  await callback.answer()
  await callback.message.delete()
