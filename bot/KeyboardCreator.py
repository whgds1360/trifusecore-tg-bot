from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import final


@final
class KeyboardCreator():
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🌐 ВК -> TG пересылка", callback_data="forward_menu"),
                    InlineKeyboardButton(text="✉️ Временная почта", callback_data="temp_mail_menu"),
                    InlineKeyboardButton(text="🤖 Нейро", callback_data="ai_menu")
                ],
                [
                    InlineKeyboardButton(text="ℹ️ Инфо", callback_data="info")
                ],
                [
                    InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
                ]
            ]
        )
